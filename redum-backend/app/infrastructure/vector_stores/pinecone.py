from typing import Any, Dict, List

from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings
from app.core.vector_store import VectorStoreProtocol


class PineconeVectorStore(VectorStoreProtocol):
    """Pinecone implementation of VectorStoreProtocol."""

    INDEX_NAME = "tasks"

    def __init__(
        self,
        *,
        settings=None,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        self.settings = settings or get_settings()
        if not self.settings.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY must be configured to use PineconeVectorStore")

        self._client = Pinecone(api_key=self.settings.PINECONE_API_KEY)
        
        # Check if index exists, create if not
        existing_indexes = [i.name for i in self._client.list_indexes()]
        if self.INDEX_NAME not in existing_indexes:
            from pinecone import ServerlessSpec
            # Assuming serverless for simplicity as per typical new setup
            # Ideally we'd config this, but for now we default to aws/us-east-1 or similar
            # based on env or hardcoded for the "free tier setup" requirement.
            # The user config has PINECONE_ENV="us-east-1", which matches serverless aws.
            
            cloud = "aws"
            region = self.settings.PINECONE_ENV if self.settings.PINECONE_ENV else "us-east-1"
            
            self._client.create_index(
                name=self.INDEX_NAME,
                dimension=384, # all-MiniLM-L6-v2 dimension
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=cloud,
                    region=region
                )
            )
            
        self._index = self._client.Index(self.INDEX_NAME)
        
        self._model = SentenceTransformer(embedding_model)

    def add_documents(
        self,
        ids: List[str],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        embeddings = self._model.encode(documents).tolist()
        vectors = []
        for i, doc_id in enumerate(ids):
            vectors.append({
                "id": doc_id,
                "values": embeddings[i],
                "metadata": {**metadatas[i], "text": documents[i]}
            })
        
        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i : i + batch_size]
            self._index.upsert(vectors=batch)

    def query(
        self,
        query_texts: List[str],
        where: Dict[str, Any],
        n_results: int,
    ) -> Dict[str, Any]:
        query_embeddings = self._model.encode(query_texts).tolist()
        
        results = {"ids": [], "documents": [], "metadatas": []}
        
        # Pinecone queries one vector at a time usually, or we map results back
        # For simplicity, assuming single query text for now or loop
        ids_list = []
        docs_list = []
        metas_list = []

        for embedding in query_embeddings:
            response = self._index.query(
                vector=embedding,
                top_k=n_results,
                filter=where if where else None,
                include_metadata=True
            )
            
            current_ids = []
            current_docs = []
            current_metas = []
            
            for match in response.matches:
                current_ids.append(match.id)
                current_metas.append(match.metadata)
                # We stored text in metadata
                current_docs.append(match.metadata.get("text", ""))
            
            ids_list.append(current_ids)
            docs_list.append(current_docs)
            metas_list.append(current_metas)

        return {
            "ids": ids_list,
            "documents": docs_list,
            "metadatas": metas_list
        }
