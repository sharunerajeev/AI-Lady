"""
API routes for the AI Insurance Assistant.
"""

from typing import Dict, Any
from datetime import datetime
import uuid
from fastapi import APIRouter, HTTPException, status
from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    ConversationHistoryResponse,
    HealthResponse,
    ErrorResponse,
)
from app.services.ai_service import ai_service
from app.services.database_service import db_service
from app.config import get_settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    settings = get_settings()

    # Check which providers are configured
    providers_status = {
        "fallback": True,  # Always available
        "ollama": False,
        "azure": bool(
            settings.azure_openai_api_key
            and settings.azure_openai_endpoint
            and settings.azure_openai_api_key != "your_azure_api_key_here"
        ),
    }

    # Try to check if Ollama is running
    try:
        import httpx

        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{settings.ollama_base_url}/api/tags")
            if response.status_code == 200:
                providers_status["ollama"] = True
    except:
        pass

    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version,
        azure_configured=providers_status["azure"],
        model_provider=settings.model_provider,
        available_providers=providers_status,
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for user interactions.

    - **message**: User's message/question
    - **session_id**: Optional session ID for conversation continuity
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Get conversation history
        history = await db_service.get_conversation_history(session_id, limit=5)
        conversation_history = [
            {"user": conv.user_message, "assistant": conv.assistant_message}
            for conv in history
        ]

        # Get AI response
        ai_response = await ai_service.get_response(
            request.message, conversation_history, provider=request.provider
        )

        # Save conversation
        await db_service.save_conversation(
            session_id=session_id,
            user_message=request.message,
            assistant_message=ai_response["response"],
        )

        return ChatResponse(
            response=ai_response["response"],
            session_id=session_id,
            sources=ai_response.get("sources", []),
            model=ai_response["model"],
            provider=ai_response.get("provider", "unknown"),
            timestamp=datetime.utcnow(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}",
        )


@router.get("/conversations/{session_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(session_id: str, limit: int = 10):
    """
    Get conversation history for a session.

    - **session_id**: Session ID to retrieve history for
    - **limit**: Maximum number of conversations to return
    """
    try:
        conversations = await db_service.get_conversation_history(session_id, limit)

        conversation_list = [
            {
                "id": conv.id,
                "user_message": conv.user_message,
                "assistant_message": conv.assistant_message,
                "timestamp": conv.timestamp.isoformat(),
                "rating": conv.rating,
            }
            for conv in conversations
        ]

        return ConversationHistoryResponse(
            session_id=session_id,
            conversations=conversation_list,
            count=len(conversation_list),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversation history: {str(e)}",
        )


@router.post("/conversations/{conversation_id}/rate")
async def rate_conversation(conversation_id: int, rating: int):
    """
    Rate a conversation (1-5 stars).

    - **conversation_id**: ID of the conversation to rate
    - **rating**: Rating value (1-5)
    """
    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5",
        )

    try:
        conversation = await db_service.rate_conversation(conversation_id, rating)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
            )

        return {"message": "Rating saved successfully", "rating": rating}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving rating: {str(e)}",
        )
