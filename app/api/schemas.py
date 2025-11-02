"""
Pydantic schemas for API request/response validation.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    session_id: Optional[str] = Field(
        None, description="Session ID for conversation tracking"
    )
    provider: Optional[str] = Field(
        None, description="AI provider to use: 'fallback', 'ollama', or 'azure'"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str = Field(..., description="AI assistant response")
    session_id: str = Field(..., description="Session ID")
    sources: List[Dict[str, Any]] = Field(
        default_factory=list, description="Source FAQs used"
    )
    model: str = Field(..., description="Model used for response")
    provider: str = Field(..., description="AI provider used")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history."""

    session_id: str
    conversations: List[Dict[str, Any]]
    count: int


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str
    app_name: str
    version: str
    azure_configured: bool
    model_provider: str = Field(..., description="Current model provider")
    available_providers: Dict[str, bool] = Field(
        default_factory=dict, description="Status of each AI provider"
    )


class ErrorResponse(BaseModel):
    """Response model for errors."""

    error: str
    detail: Optional[str] = None
