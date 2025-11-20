import unittest
from unittest.mock import MagicMock, patch

from app.infrastructure.vector_stores.chroma import ChromaVectorStore
from app.infrastructure.vector_stores.pinecone import PineconeVectorStore


class TestChromaVectorStore(unittest.TestCase):
    @patch("app.infrastructure.vector_stores.chroma.chromadb.PersistentClient")
    def test_add_documents(self, mock_client):
        mock_collection = MagicMock()
        mock_client.return_value.get_or_create_collection.return_value = mock_collection
        
        store = ChromaVectorStore()
        store.add_documents(["1"], ["doc"], [{"meta": "data"}])
        
        mock_collection.upsert.assert_called_once_with(
            ids=["1"],
            documents=["doc"],
            metadatas=[{"meta": "data"}]
        )

    @patch("app.infrastructure.vector_stores.chroma.chromadb.PersistentClient")
    def test_query(self, mock_client):
        mock_collection = MagicMock()
        mock_client.return_value.get_or_create_collection.return_value = mock_collection
        
        store = ChromaVectorStore()
        store.query(["query"], {}, 5)
        
        mock_collection.query.assert_called_once_with(
            query_texts=["query"],
            where={},
            n_results=5
        )


class TestPineconeVectorStore(unittest.TestCase):
    @patch("app.infrastructure.vector_stores.pinecone.Pinecone")
    @patch("app.infrastructure.vector_stores.pinecone.SentenceTransformer")
    def test_add_documents(self, mock_sentence_transformer, mock_pinecone):
        # Setup mocks
        mock_index = MagicMock()
        mock_pinecone.return_value.Index.return_value = mock_index
        
        mock_model = MagicMock()
        mock_sentence_transformer.return_value = mock_model
        mock_model.encode.return_value.tolist.return_value = [[0.1, 0.2]]

        # Setup settings with API key
        settings = MagicMock()
        settings.PINECONE_API_KEY = "test-key"
        
        store = PineconeVectorStore(settings=settings)
        store.add_documents(["1"], ["doc"], [{"meta": "data"}])
        
        mock_index.upsert.assert_called()
        call_args = mock_index.upsert.call_args[1]
        self.assertEqual(len(call_args['vectors']), 1)
        self.assertEqual(call_args['vectors'][0]['id'], "1")
        self.assertEqual(call_args['vectors'][0]['values'], [0.1, 0.2])
        self.assertEqual(call_args['vectors'][0]['metadata']['text'], "doc")

    @patch("app.infrastructure.vector_stores.pinecone.Pinecone")
    @patch("app.infrastructure.vector_stores.pinecone.SentenceTransformer")
    def test_query(self, mock_sentence_transformer, mock_pinecone):
        # Setup mocks
        mock_index = MagicMock()
        mock_pinecone.return_value.Index.return_value = mock_index
        
        mock_model = MagicMock()
        mock_sentence_transformer.return_value = mock_model
        mock_model.encode.return_value.tolist.return_value = [[0.1, 0.2]]
        
        mock_match = MagicMock()
        mock_match.id = "1"
        mock_match.metadata = {"text": "doc", "meta": "data"}
        mock_index.query.return_value.matches = [mock_match]

        # Setup settings
        settings = MagicMock()
        settings.PINECONE_API_KEY = "test-key"
        
        store = PineconeVectorStore(settings=settings)
        result = store.query(["query"], {}, 5)
        
        self.assertEqual(result["ids"], [["1"]])
        self.assertEqual(result["documents"], [["doc"]])
