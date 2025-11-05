"""
Database service for managing conversations and database operations.
"""

import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select, desc, update
from app.models.database import Base, Conversation, UserPreference, Recommendation, ConversationContext
from app.config import get_settings


class DatabaseService:
    """Service for database operations."""

    def __init__(self):
        """Initialize database service."""
        settings = get_settings()
        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
        )
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def init_db(self):
        """Initialize database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def save_conversation(
        self, 
        session_id: str, 
        user_message: str, 
        assistant_message: str,
        is_recommendation_flow: bool = False,
        context_data: Optional[Dict[str, Any]] = None
    ) -> Conversation:
        """Save a conversation to the database."""
        async with self.async_session() as session:
            conversation = Conversation(
                session_id=session_id,
                user_message=user_message,
                assistant_message=assistant_message,
                timestamp=datetime.utcnow(),
                is_recommendation_flow=1 if is_recommendation_flow else 0,
                context_data=json.dumps(context_data) if context_data else None
            )
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            return conversation

    async def get_conversation_history(
        self, session_id: str, limit: int = 10
    ) -> List[Conversation]:
        """Get conversation history for a session."""
        async with self.async_session() as session:
            stmt = (
                select(Conversation)
                .where(Conversation.session_id == session_id)
                .order_by(desc(Conversation.timestamp))
                .limit(limit)
            )
            result = await session.execute(stmt)
            conversations = result.scalars().all()
            return list(reversed(conversations))

    async def rate_conversation(
        self, conversation_id: int, rating: int
    ) -> Optional[Conversation]:
        """Rate a conversation."""
        async with self.async_session() as session:
            stmt = select(Conversation).where(Conversation.id == conversation_id)
            result = await session.execute(stmt)
            conversation = result.scalar_one_or_none()

            if conversation:
                conversation.rating = rating
                await session.commit()
                await session.refresh(conversation)

            return conversation

    async def close(self):
        """Close database connections."""
        await self.engine.dispose()

    # ========== Conversation Context Methods ==========
    
    async def get_conversation_context(self, session_id: str) -> Optional[ConversationContext]:
        """Get conversation context for a session."""
        async with self.async_session() as session:
            stmt = select(ConversationContext).where(ConversationContext.session_id == session_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
    
    async def save_conversation_context(
        self,
        session_id: str,
        current_flow: Optional[str] = None,
        insurance_type: Optional[str] = None,
        current_question_index: int = 0,
        collected_answers: Optional[Dict[str, Any]] = None,
        awaiting_response_for: Optional[str] = None
    ) -> ConversationContext:
        """Save or update conversation context."""
        async with self.async_session() as session:
            stmt = select(ConversationContext).where(ConversationContext.session_id == session_id)
            result = await session.execute(stmt)
            context = result.scalar_one_or_none()
            
            if context:
                # Update existing
                context.current_flow = current_flow
                context.insurance_type = insurance_type
                context.current_question_index = current_question_index
                context.collected_answers = json.dumps(collected_answers) if collected_answers else None
                context.awaiting_response_for = awaiting_response_for
                context.updated_at = datetime.utcnow()
            else:
                # Create new
                context = ConversationContext(
                    session_id=session_id,
                    current_flow=current_flow,
                    insurance_type=insurance_type,
                    current_question_index=current_question_index,
                    collected_answers=json.dumps(collected_answers) if collected_answers else None,
                    awaiting_response_for=awaiting_response_for
                )
                session.add(context)
            
            await session.commit()
            await session.refresh(context)
            return context
    
    async def clear_conversation_context(self, session_id: str) -> None:
        """Clear conversation context for a session."""
        async with self.async_session() as session:
            stmt = select(ConversationContext).where(ConversationContext.session_id == session_id)
            result = await session.execute(stmt)
            context = result.scalar_one_or_none()
            
            if context:
                await session.delete(context)
                await session.commit()
    
    # ========== User Preference Methods ==========
    
    async def save_user_preference(
        self,
        session_id: str,
        insurance_type: str,
        requirements: Dict[str, Any]
    ) -> UserPreference:
        """Save user preferences for an insurance type."""
        async with self.async_session() as session:
            preference = UserPreference(
                session_id=session_id,
                insurance_type=insurance_type,
                requirements=json.dumps(requirements)
            )
            session.add(preference)
            await session.commit()
            await session.refresh(preference)
            return preference
    
    async def get_user_preferences(
        self,
        session_id: str,
        insurance_type: Optional[str] = None
    ) -> List[UserPreference]:
        """Get user preferences, optionally filtered by insurance type."""
        async with self.async_session() as session:
            stmt = select(UserPreference).where(UserPreference.session_id == session_id)
            
            if insurance_type:
                stmt = stmt.where(UserPreference.insurance_type == insurance_type)
            
            stmt = stmt.order_by(desc(UserPreference.updated_at))
            result = await session.execute(stmt)
            return list(result.scalars().all())
    
    # ========== Recommendation Methods ==========
    
    async def save_recommendation(
        self,
        session_id: str,
        insurance_type: str,
        product_id: str,
        product_name: str,
        match_score: float,
        match_reasons: List[str],
        user_requirements: Dict[str, Any]
    ) -> Recommendation:
        """Save a product recommendation."""
        async with self.async_session() as session:
            recommendation = Recommendation(
                session_id=session_id,
                insurance_type=insurance_type,
                product_id=product_id,
                product_name=product_name,
                match_score=match_score,
                match_reasons=json.dumps(match_reasons),
                user_requirements=json.dumps(user_requirements),
                user_feedback="pending"
            )
            session.add(recommendation)
            await session.commit()
            await session.refresh(recommendation)
            return recommendation
    
    async def get_recommendation_history(
        self,
        session_id: str,
        insurance_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Recommendation]:
        """Get recommendation history for a session."""
        async with self.async_session() as session:
            stmt = select(Recommendation).where(Recommendation.session_id == session_id)
            
            if insurance_type:
                stmt = stmt.where(Recommendation.insurance_type == insurance_type)
            
            stmt = stmt.order_by(desc(Recommendation.recommended_at)).limit(limit)
            result = await session.execute(stmt)
            return list(result.scalars().all())
    
    async def update_recommendation_feedback(
        self,
        recommendation_id: int,
        feedback: str,
        notes: Optional[str] = None
    ) -> Optional[Recommendation]:
        """Update feedback for a recommendation."""
        async with self.async_session() as session:
            stmt = select(Recommendation).where(Recommendation.id == recommendation_id)
            result = await session.execute(stmt)
            recommendation = result.scalar_one_or_none()
            
            if recommendation:
                recommendation.user_feedback = feedback
                recommendation.feedback_notes = notes
                await session.commit()
                await session.refresh(recommendation)
            
            return recommendation


# Global database instance
db_service = DatabaseService()
