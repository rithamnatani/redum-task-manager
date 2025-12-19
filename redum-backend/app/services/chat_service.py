"""Conversational AI Chat Service using LCEL (LangChain Expression Language)."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings
from app.core.vector_store import VectorStoreProtocol


logger = logging.getLogger(__name__)


@dataclass
class ChatMessage:
    """Represents a single chat message."""

    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ChatHistory:
    """Holds conversation history for a chat session."""

    messages: List[ChatMessage] = field(default_factory=list)
    session_id: Optional[str] = None

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the history."""
        self.messages.append(ChatMessage(role=role, content=content))

    def to_langchain_messages(self) -> List[Any]:
        """Convert history to LangChain message format."""
        lc_messages = []
        for msg in self.messages:
            if msg.role == "user":
                lc_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                lc_messages.append(AIMessage(content=msg.content))
        return lc_messages


class ChatService:
    """
    Conversational AI service using LCEL for building the chat chain.
    
    Chain architecture:
        ChatHistory + Query → Retrieve Context → Generate Response
    """

    def __init__(
        self,
        vector_store: VectorStoreProtocol,
        *,
        settings=None,
    ) -> None:
        self.settings = settings or get_settings()
        self.vector_store = vector_store

        if not self.settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY must be configured to use ChatService")

        # Initialize LangChain LLM
        self._llm = ChatGoogleGenerativeAI(
            model=self.settings.GEMINI_MODEL,
            google_api_key=self.settings.GEMINI_API_KEY,
            temperature=0.7,
        )

        # Build the LCEL chain
        self._chain = self._build_lcel_chain()

    def _build_lcel_chain(self):
        """
        Build the LCEL chain:
        ChatHistory + Query → Retrieve Context → Generate Response
        """
        # System prompt with context and history placeholders
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a helpful AI assistant for task management. 
You help users manage their tasks, answer questions about their tasks, 
and provide suggestions based on their task history.

Here is relevant context from the user's tasks:
{context}

Use this context to provide helpful, relevant responses. 
If the context doesn't contain relevant information, still try to help the user 
with general task management advice."""
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{query}"),
        ])

        # Build the chain using LCEL
        chain = (
            RunnablePassthrough.assign(
                context=lambda x: self._retrieve_context(
                    query=x["query"],
                    user_id=x["user_id"],
                )
            )
            | prompt
            | self._llm
            | StrOutputParser()
        )

        return chain

    def _retrieve_context(self, query: str, user_id: int) -> str:
        """Retrieve relevant task context from the vector store."""
        try:
            results = self.vector_store.query(
                query_texts=[query],
                where={"user_id": user_id},
                n_results=5,
            )
        except Exception as exc:
            logger.warning("Vector store query failed: %s", exc)
            return "No relevant task context available."

        documents = results.get("documents", [[]])[0]
        if not documents:
            return "No relevant task context available."

        # Format context as a readable list
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"{i}. {doc}")

        return "\n".join(context_parts)

    def chat(
        self,
        query: str,
        history: ChatHistory,
        user_id: int,
    ) -> str:
        """
        Process a chat query with history and context retrieval.
        
        Args:
            query: The user's current message/question
            history: The conversation history
            user_id: The user's ID for filtering relevant tasks
            
        Returns:
            The AI assistant's response
        """
        try:
            # Convert history to LangChain format
            lc_history = history.to_langchain_messages()

            # Invoke the LCEL chain
            response = self._chain.invoke({
                "query": query,
                "user_id": user_id,
                "chat_history": lc_history,
            })

            return response

        except Exception as exc:
            logger.error("Chat service error: %s", exc)
            raise ValueError(f"Chat service encountered an error: {exc}") from exc

    async def achat(
        self,
        query: str,
        history: ChatHistory,
        user_id: int,
    ) -> str:
        """
        Async version of chat for non-blocking operation.
        
        Args:
            query: The user's current message/question
            history: The conversation history
            user_id: The user's ID for filtering relevant tasks
            
        Returns:
            The AI assistant's response
        """
        try:
            lc_history = history.to_langchain_messages()

            response = await self._chain.ainvoke({
                "query": query,
                "user_id": user_id,
                "chat_history": lc_history,
            })

            return response

        except Exception as exc:
            logger.error("Async chat service error: %s", exc)
            raise ValueError(f"Chat service encountered an error: {exc}") from exc
