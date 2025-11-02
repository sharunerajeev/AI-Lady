"""
Database service for managing conversations and database operations.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select, desc
from app.models.database import Base, Conversation
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
        self, session_id: str, user_message: str, assistant_message: str
    ) -> Conversation:
        """Save a conversation to the database."""
        async with self.async_session() as session:
            conversation = Conversation(
                session_id=session_id,
                user_message=user_message,
                assistant_message=assistant_message,
                timestamp=datetime.utcnow(),
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


# Global database instance
db_service = DatabaseService()
