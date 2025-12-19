"""Unit tests for ChatService."""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from app.services.chat_service import ChatService, ChatMessage, ChatHistory


class TestChatMessage(unittest.TestCase):
    """Tests for ChatMessage dataclass."""

    def test_create_message(self):
        msg = ChatMessage(role="user", content="Hello")
        self.assertEqual(msg.role, "user")
        self.assertEqual(msg.content, "Hello")
        self.assertIsInstance(msg.timestamp, datetime)

    def test_create_message_with_timestamp(self):
        ts = datetime(2023, 1, 1, 12, 0, 0)
        msg = ChatMessage(role="assistant", content="Hi there", timestamp=ts)
        self.assertEqual(msg.timestamp, ts)


class TestChatHistory(unittest.TestCase):
    """Tests for ChatHistory dataclass."""

    def test_empty_history(self):
        history = ChatHistory()
        self.assertEqual(len(history.messages), 0)
        self.assertIsNone(history.session_id)

    def test_add_message(self):
        history = ChatHistory()
        history.add_message("user", "Hello")
        history.add_message("assistant", "Hi there")
        self.assertEqual(len(history.messages), 2)
        self.assertEqual(history.messages[0].role, "user")
        self.assertEqual(history.messages[1].role, "assistant")

    def test_to_langchain_messages(self):
        history = ChatHistory()
        history.add_message("user", "Hello")
        history.add_message("assistant", "Hi")
        history.add_message("user", "How are you?")

        lc_msgs = history.to_langchain_messages()
        self.assertEqual(len(lc_msgs), 3)
        self.assertEqual(lc_msgs[0].content, "Hello")
        self.assertEqual(lc_msgs[1].content, "Hi")
        self.assertEqual(lc_msgs[2].content, "How are you?")


class TestChatService(unittest.TestCase):
    """Tests for ChatService."""

    @patch("app.services.chat_service.ChatGoogleGenerativeAI")
    def test_init_without_api_key(self, mock_llm):
        """Test that ChatService raises error without API key."""
        mock_vector_store = MagicMock()
        settings = MagicMock()
        settings.GEMINI_API_KEY = ""

        with self.assertRaises(ValueError) as context:
            ChatService(vector_store=mock_vector_store, settings=settings)

        self.assertIn("GEMINI_API_KEY", str(context.exception))

    @patch("app.services.chat_service.ChatGoogleGenerativeAI")
    def test_init_success(self, mock_llm):
        """Test successful ChatService initialization."""
        mock_vector_store = MagicMock()
        settings = MagicMock()
        settings.GEMINI_API_KEY = "test-key"
        settings.GEMINI_MODEL = "gemini-2.5-flash"

        service = ChatService(vector_store=mock_vector_store, settings=settings)

        self.assertIsNotNone(service._chain)
        mock_llm.assert_called_once()

    @patch("app.services.chat_service.ChatGoogleGenerativeAI")
    def test_retrieve_context(self, mock_llm):
        """Test context retrieval from vector store."""
        mock_vector_store = MagicMock()
        mock_vector_store.query.return_value = {
            "documents": [["Task 1: Buy groceries", "Task 2: Call mom"]]
        }

        settings = MagicMock()
        settings.GEMINI_API_KEY = "test-key"
        settings.GEMINI_MODEL = "gemini-2.5-flash"

        service = ChatService(vector_store=mock_vector_store, settings=settings)

        context = service._retrieve_context("what tasks do I have?", user_id=1)

        self.assertIn("Buy groceries", context)
        self.assertIn("Call mom", context)
        mock_vector_store.query.assert_called_once()

    @patch("app.services.chat_service.ChatGoogleGenerativeAI")
    def test_retrieve_context_empty(self, mock_llm):
        """Test context retrieval with no results."""
        mock_vector_store = MagicMock()
        mock_vector_store.query.return_value = {"documents": [[]]}

        settings = MagicMock()
        settings.GEMINI_API_KEY = "test-key"
        settings.GEMINI_MODEL = "gemini-2.5-flash"

        service = ChatService(vector_store=mock_vector_store, settings=settings)

        context = service._retrieve_context("random query", user_id=1)

        self.assertEqual(context, "No relevant task context available.")

    @patch("app.services.chat_service.ChatGoogleGenerativeAI")
    def test_retrieve_context_error(self, mock_llm):
        """Test context retrieval when vector store fails."""
        mock_vector_store = MagicMock()
        mock_vector_store.query.side_effect = Exception("Connection error")

        settings = MagicMock()
        settings.GEMINI_API_KEY = "test-key"
        settings.GEMINI_MODEL = "gemini-2.5-flash"

        service = ChatService(vector_store=mock_vector_store, settings=settings)

        context = service._retrieve_context("query", user_id=1)

        self.assertEqual(context, "No relevant task context available.")

    @patch("app.services.chat_service.ChatGoogleGenerativeAI")
    def test_chat(self, mock_llm_class):
        """Test chat method invokes the chain correctly."""
        mock_vector_store = MagicMock()
        mock_vector_store.query.return_value = {"documents": [["Existing task"]]}

        settings = MagicMock()
        settings.GEMINI_API_KEY = "test-key"
        settings.GEMINI_MODEL = "gemini-2.5-flash"

        # Mock the LLM response
        mock_llm_instance = MagicMock()
        mock_llm_class.return_value = mock_llm_instance

        service = ChatService(vector_store=mock_vector_store, settings=settings)

        # Mock the chain invoke
        with patch.object(service, "_chain") as mock_chain:
            mock_chain.invoke.return_value = "Here are your tasks..."

            history = ChatHistory()
            history.add_message("user", "Hi")
            history.add_message("assistant", "Hello! How can I help?")

            response = service.chat(
                query="What tasks do I have?",
                history=history,
                user_id=1,
            )

            self.assertEqual(response, "Here are your tasks...")
            mock_chain.invoke.assert_called_once()

            # Verify the invoke was called with correct structure
            call_args = mock_chain.invoke.call_args[0][0]
            self.assertEqual(call_args["query"], "What tasks do I have?")
            self.assertEqual(call_args["user_id"], 1)
            self.assertEqual(len(call_args["chat_history"]), 2)


if __name__ == "__main__":
    unittest.main()
