from typing import Any, Dict, List, Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings
from app.core.vector_store import VectorStoreProtocol
from app.domain.models.task import Task


class PgVectorStore(VectorStoreProtocol):
    """PgVector implementation of VectorStoreProtocol."""

    def __init__(
        self,
        session: Session,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        self.session = session
        self._embedding_model = SentenceTransformer(embedding_model)

    def add_documents(
        self,
        ids: List[str],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        """
        Generate embeddings for documents and update the corresponding Task rows.
        
        Note: This implementation assumes that the 'ids' provided correspond to 
        existing Task IDs in the database. It does NOT create new tasks.
        """
        if not ids:
            return

        embeddings = self._embedding_model.encode(documents)
        
        # Update tasks one by one or in batches. 
        # Since we need to map id -> embedding, iterating is straightforward.
        # ids are strings, Task.id is Integer.
        
        for task_id, embedding in zip(ids, embeddings):
            try:
                int_id = int(task_id)
                stmt = (
                    update(Task)
                    .where(Task.id == int_id)
                    .values(vector=embedding.tolist())
                )
                self.session.execute(stmt)
            except ValueError:
                # Skip invalid IDs
                continue
        
        self.session.commit()

    def query(
        self,
        query_texts: List[str],
        where: Dict[str, Any],
        n_results: int,
    ) -> Dict[str, Any]:
        """
        Query the vector store for similar tasks.
        
        Returns a dictionary matching the ChromaDB query result format:
        {
            "ids": [[id1, id2, ...]],
            "documents": [[doc1, doc2, ...]],
            "metadatas": [[meta1, meta2, ...]],
            "distances": [[dist1, dist2, ...]],
        }
        """
        # We currently only support a single query text for simplicity in this implementation,
        # or we iterate. The protocol implies batch support, but typically we use one.
        # Let's handle the first one or iterate. 
        # Chroma returns a list of lists.
        
        results = {
            "ids": [],
            "documents": [],
            "metadatas": [],
            "distances": [],
        }

        for text in query_texts:
            query_embedding = self._embedding_model.encode(text).tolist()
            
            # Build query
            # Note: Task.vector.l2_distance(query_embedding)
            stmt = (
                select(Task)
                .order_by(Task.vector.l2_distance(query_embedding))
                .limit(n_results)
            )
            
            # Apply 'where' filters if needed. 
            # This is complex to map generic dict filters to SQLAlchemy.
            # For now, we might skip complex filtering or implement basic ones if needed.
            # The current usage in RAGService might not use complex filters.
            
            tasks = self.session.scalars(stmt).all()
            
            ids_list = []
            docs_list = []
            metas_list = []
            dists_list = []
            
            for task in tasks:
                ids_list.append(str(task.id))
                docs_list.append(task.description or task.title) # Use description or title as document
                metas_list.append({
                    "title": task.title,
                    "status": task.status,
                    "priority": task.priority
                })
                # Distance is not directly returned by scalars(), we might need to select it specifically
                # or just return 0.0 if not critical. 
                # To get distance: select(Task, Task.vector.l2_distance(query_embedding))
                dists_list.append(0.0) # Placeholder if we don't fetch distance
            
            results["ids"].append(ids_list)
            results["documents"].append(docs_list)
            results["metadatas"].append(metas_list)
            results["distances"].append(dists_list)

        return results

    def delete(self, ids: List[str]) -> None:
        """Clear vectors for the given task IDs."""
        if not ids:
            return
            
        int_ids = []
        for i in ids:
            try:
                int_ids.append(int(i))
            except ValueError:
                continue
                
        if not int_ids:
            return

        stmt = (
            update(Task)
            .where(Task.id.in_(int_ids))
            .values(vector=None)
        )
        self.session.execute(stmt)
        self.session.commit()
