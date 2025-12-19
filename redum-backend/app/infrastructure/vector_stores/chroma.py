from pathlib import Path
from typing import Any, Dict, List

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from app.core.config import get_settings
from app.core.vector_store import VectorStoreProtocol


class _EmbeddingFunctionWrapper(EmbeddingFunction[Documents]):
    """Adapter to plug sentence-transformers into ChromaDB."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self._function = SentenceTransformerEmbeddingFunction(model_name=model_name)

    def __call__(self, input: Documents) -> Embeddings:  # noqa: A003 - Chroma signature
        return self._function(input)


class ChromaVectorStore(VectorStoreProtocol):
    """ChromaDB implementation of VectorStoreProtocol."""

    COLLECTION_NAME = "tasks"

    def __init__(
        self,
        *,
        settings=None,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        self.settings = settings or get_settings()
        storage_path = Path(self.settings.CHROMA_DB_PATH).expanduser().resolve()
        storage_path.mkdir(parents=True, exist_ok=True)
        
        self._client = chromadb.PersistentClient(path=str(storage_path))
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            embedding_function=_EmbeddingFunctionWrapper(model_name=embedding_model),
        )

    def add_documents(
        self,
        ids: List[str],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        self._collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )

    def query(
        self,
        query_texts: List[str],
        where: Dict[str, Any],
        n_results: int,
    ) -> Dict[str, Any]:
        return self._collection.query(
            query_texts=query_texts,
            where=where,
            n_results=n_results,
        )

    def delete(self, ids: List[str]) -> None:
        self._collection.delete(ids=ids)
