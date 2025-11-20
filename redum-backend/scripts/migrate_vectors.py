import logging
import sys
from pathlib import Path

# Add app to python path
sys.path.append(str(Path(__file__).parent.parent))

import chromadb
from app.core.config import get_settings
from app.infrastructure.vector_stores.pinecone import PineconeVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    settings = get_settings()
    
    logger.info("Connecting to ChromaDB...")
    storage_path = Path(settings.CHROMA_DB_PATH).expanduser().resolve()
    if not storage_path.exists():
        logger.error(f"ChromaDB path {storage_path} does not exist.")
        return

    chroma_client = chromadb.PersistentClient(path=str(storage_path))
    try:
        collection = chroma_client.get_collection("tasks")
    except Exception as e:
        logger.error(f"Could not get 'tasks' collection: {e}")
        return

    # Fetch all documents
    data = collection.get()
    ids = data["ids"]
    documents = data["documents"]
    metadatas = data["metadatas"]

    if not ids:
        logger.info("No documents found in ChromaDB.")
        return

    logger.info(f"Found {len(ids)} documents in ChromaDB.")

    logger.info("Initializing PineconeVectorStore...")
    try:
        pinecone_store = PineconeVectorStore(settings=settings)
    except ValueError as e:
        logger.error(f"Failed to initialize Pinecone: {e}")
        return

    logger.info("Migrating documents to Pinecone...")
    # PineconeVectorStore.add_documents will re-generate embeddings
    pinecone_store.add_documents(ids=ids, documents=documents, metadatas=metadatas)

    logger.info("Migration complete.")

if __name__ == "__main__":
    migrate()
