"""Chat API endpoint for conversational AI."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.use_cases.auth.auth_service import AuthService
from app.services.chat_service import ChatService, ChatHistory, ChatMessage
from app.core.config import get_settings
from app.infrastructure.vector_stores.pgvector_store import PgVectorStore


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessageSchema(BaseModel):
    """Schema for a chat message."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str
    history: List[ChatMessageSchema] = []


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    response: str
    history: List[ChatMessageSchema]


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user),
):
    """
    Process a chat message and return AI response.
    
    The chat uses conversation history and retrieves relevant task context
    to provide helpful responses.
    """
    settings = get_settings()
    
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="AI chat service is not configured"
        )
    
    try:
        # Initialize vector store and chat service
        vector_store = PgVectorStore(session=db)
        chat_service = ChatService(vector_store=vector_store, settings=settings)
        
        # Build chat history from request
        history = ChatHistory()
        for msg in request.history:
            history.add_message(role=msg.role, content=msg.content)
        
        # Get response from chat service
        response_text = chat_service.chat(
            query=request.message,
            history=history,
            user_id=current_user.id,
        )
        
        # Build updated history for response
        updated_history = [
            *request.history,
            ChatMessageSchema(role="user", content=request.message),
            ChatMessageSchema(role="assistant", content=response_text),
        ]
        
        return ChatResponse(
            response=response_text,
            history=updated_history,
        )
        
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat service error: {str(e)}"
        )
