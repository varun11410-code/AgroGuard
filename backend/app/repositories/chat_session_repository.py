"""
AgroGuard Backend - Chat Session Repository

Handles database operations for the ChatSession model.
"""
from typing import List, Optional
import uuid
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from app.models.chat_session import ChatSession

class ChatSessionRepository:
    @staticmethod
    def create(session: ChatSession) -> ChatSession:
        """
        Persists a new ChatSession to the database.
        Raises ValueError if there's an integrity error or validation failure.
        """
        try:
            db.session.add(session)
            db.session.commit()
            return session
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Failed to create chat session: {str(e)}")

    @staticmethod
    def get_by_id_and_user(session_id: str, user_id: str) -> Optional[ChatSession]:
        """
        Retrieves a ChatSession by its ID, ensuring it belongs to the specified user.
        Returns None if the session does not exist or does not belong to the user.
        """
        try:
            sid = uuid.UUID(session_id)
            uid = uuid.UUID(user_id)
        except ValueError:
            return None

        return ChatSession.query.filter_by(id=sid, user_id=uid).first()

    @staticmethod
    def get_by_user(user_id: str) -> List[ChatSession]:
        """
        Retrieves all ChatSessions belonging to a specific user, ordered by most recent first.
        """
        try:
            uid = uuid.UUID(user_id)
        except ValueError:
            return []

        return ChatSession.query.filter_by(user_id=uid).order_by(ChatSession.created_at.desc()).all()
