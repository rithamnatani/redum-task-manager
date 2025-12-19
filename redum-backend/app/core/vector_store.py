from typing import Any, Dict, List, Protocol, runtime_checkable

@runtime_checkable
class VectorStoreProtocol(Protocol):
    """Protocol for vector store implementations."""

    def add_documents(
        self,
        ids: List[str],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        """Add documents to the vector store."""
        ...

    def query(
        self,
        query_texts: List[str],
        where: Dict[str, Any],
        n_results: int,
    ) -> Dict[str, Any]:
        """Query the vector store."""
        ...

    def delete(self, ids: List[str]) -> None:
        """Delete documents from the vector store."""
        ...
