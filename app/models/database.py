"""
Database models for the AI Insurance Assistant.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Text, Integer, JSON, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class Conversation(Base):
    """Model for storing conversation history."""

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    user_message: Mapped[str] = mapped_column(Text, nullable=False)
    assistant_message: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    # Track if this is part of a recommendation flow
    is_recommendation_flow: Mapped[Optional[bool]] = mapped_column(Integer, default=0, nullable=True)
    context_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, session_id={self.session_id})>"


class UserPreference(Base):
    """Model for storing user preferences and requirements."""

    __tablename__ = "user_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    insurance_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    requirements: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<UserPreference(id={self.id}, session_id={self.session_id}, type={self.insurance_type})>"


class Recommendation(Base):
    """Model for storing recommendation history."""

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    insurance_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    product_id: Mapped[str] = mapped_column(String(100), nullable=False)
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    match_score: Mapped[float] = mapped_column(Float, nullable=False)
    match_reasons: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string
    user_requirements: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string
    recommended_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    user_feedback: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # accepted, rejected, pending
    feedback_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Recommendation(id={self.id}, product={self.product_name}, score={self.match_score})>"


class ConversationContext(Base):
    """Model for storing multi-turn conversation context."""

    __tablename__ = "conversation_contexts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    current_flow: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # recommendation, general_inquiry
    insurance_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    current_question_index: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    collected_answers: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    awaiting_response_for: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<ConversationContext(session_id={self.session_id}, flow={self.current_flow})>"
