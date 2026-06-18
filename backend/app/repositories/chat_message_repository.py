"""
AgroGuard Backend - Chat Message Repository

Handles database operations for the ChatMessage model.
"""
from typing import List
import uuid
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from app.models.chat_message import ChatMessage

class ChatMessageRepository:
    @staticmethod
    def create(message: ChatMessage) -> ChatMessage:
        """
        Persists a new ChatMessage to the database.
        """
        try:
            db.session.add(message)
            db.session.commit()
            return message
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to create chat message: {str(e)}")

    @staticmethod
    def get_by_session(session_id: str) -> List[ChatMessage]:
        """
        Retrieves all ChatMessages belonging to a specific session.
        Ordered chronologically by created_at, then id as a deterministic tie-breaker.
        """
        try:
            sid = uuid.UUID(session_id)
        except ValueError:
            return []

        return ChatMessage.query.filter_by(session_id=sid).order_by(
            ChatMessage.created_at.asc(),
            ChatMessage.id.asc()
        ).all()
