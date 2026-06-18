"""
AgroGuard Backend - Chat Session Service

Business logic for managing AI chat sessions.
"""
import uuid
from typing import List, Dict, Any, Optional
from app.models.chat_session import ChatSession
from app.repositories.chat_session_repository import ChatSessionRepository

class ChatSessionService:
    @staticmethod
    def create_session(user_id: str, scan_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Creates a new chat session for the specified user.
        If scan_id is provided, it creates a Mode B (diagnosis-aware) session.
        Otherwise, it creates a Mode A (general) session.
        """
        try:
            uid = uuid.UUID(user_id)
            sid = uuid.UUID(scan_id) if scan_id else None
        except ValueError:
            raise ValueError("Invalid user_id or scan_id format.")

        session = ChatSession(
            user_id=uid,
            scan_id=sid,
            expires_at=None  # Explicitly leaving as None per architectural recommendation
        )

        created_session = ChatSessionRepository.create(session)
        return ChatSessionService._serialize(created_session)

    @staticmethod
    def get_session(session_id: str, user_id: str) -> Dict[str, Any]:
        """
        Retrieves a chat session and validates ownership.
        Raises ValueError if the session is not found or unauthorized.
        """
        session = ChatSessionRepository.get_by_id_and_user(session_id, user_id)
        if not session:
            raise ValueError("Session not found or unauthorized access.")
        
        return ChatSessionService._serialize(session)

    @staticmethod
    def get_user_sessions(user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all active sessions for a user.
        """
        sessions = ChatSessionRepository.get_by_user(user_id)
        return [ChatSessionService._serialize(s) for s in sessions]

    @staticmethod
    def _serialize(session: ChatSession) -> Dict[str, Any]:
        """
        Serializes the SQLAlchemy ChatSession model into a plain Python dictionary.
        """
        return {
            "id": str(session.id),
            "user_id": str(session.user_id),
            "scan_id": str(session.scan_id) if session.scan_id else None,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "expires_at": session.expires_at.isoformat() if session.expires_at else None,
            "updated_at": session.updated_at.isoformat() if session.updated_at else None,
        }
