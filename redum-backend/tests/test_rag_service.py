import unittest
from unittest.mock import MagicMock, patch

from app.domain.schemas.task import TaskRead
from app.services.ai_service import RAGService


class TestRAGService(unittest.TestCase):
    @patch("app.services.ai_service.genai")
    def test_add_task_to_kb(self, mock_genai):
        mock_vector_store = MagicMock()
        settings = MagicMock()
        settings.GEMINI_API_KEY = "test-key"
        
        service = RAGService(vector_store=mock_vector_store, settings=settings)
        
        task = TaskRead(
            id=1,
            user_id=1,
            title="Test Task",
            priority=1,
            status="todo",
            description="desc",
            created_at="2023-01-01T00:00:00",
            due_date=None
        )
        service.add_task_to_kb(task)
        
        mock_vector_store.add_documents.assert_called_once()
        call_args = mock_vector_store.add_documents.call_args[1]
        self.assertEqual(call_args['ids'], ["1"])
        self.assertIn("Title: Test Task", call_args['documents'][0])

    @patch("app.services.ai_service.genai")
    def test_suggest_metadata(self, mock_genai):
        mock_vector_store = MagicMock()
        mock_vector_store.query.return_value = {"documents": [["existing task"]]}
        
        settings = MagicMock()
        settings.GEMINI_API_KEY = "test-key"
        
        # Mock Gemini response
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_response = MagicMock()
        mock_response.candidates = [MagicMock(content=MagicMock(parts=[MagicMock(text='{"priority": 2}')]))]
        mock_model.generate_content.return_value = mock_response
        
        service = RAGService(vector_store=mock_vector_store, settings=settings)
        
        suggestion = service.suggest_metadata(user_id=1, description="New task")
        
        self.assertEqual(suggestion.priority, 2)
        mock_vector_store.query.assert_called_once()
