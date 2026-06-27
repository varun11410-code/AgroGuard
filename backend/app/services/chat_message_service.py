"""
AgroGuard Backend - Chat Message Service

Business logic for managing chat conversation history.
"""
import uuid
from typing import List, Dict, Any
from app.models.chat_message import ChatMessage, MessageRole
from app.repositories.chat_message_repository import ChatMessageRepository
from app.services.chat_session_service import ChatSessionService
from app.core.exceptions import BadRequestException

class ChatMessageService:
    @staticmethod
    def save_message(session_id: str, user_id: str, role: MessageRole, message: str) -> Dict[str, Any]:
        """
        Saves a new message to the chat history.
        Validates session ownership before allowing the insertion.
        """
        if not message or not message.strip():
            raise BadRequestException("Message cannot be empty or whitespace.", error_code="CHAT_EMPTY_MESSAGE")

        # Validate session ownership. Raises ValueError if session is not found or unauthorized.
        ChatSessionService.get_session(session_id, user_id)

        try:
            sid = uuid.UUID(session_id)
        except ValueError:
            raise BadRequestException("Invalid session_id format.", error_code="CHAT_INVALID_SESSION_ID")

        new_message = ChatMessage(
            session_id=sid,
            role=role,
            message=message.strip()
        )

        created_message = ChatMessageRepository.create(new_message)
        return ChatMessageService._serialize(created_message)

    @staticmethod
    def get_session_history(session_id: str, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves the deterministic, chronologically ordered chat history for a session.
        Validates session ownership before returning.
        """
        # Validate session ownership
        ChatSessionService.get_session(session_id, user_id)

        messages = ChatMessageRepository.get_by_session(session_id)
        return [ChatMessageService._serialize(msg) for msg in messages]

    @staticmethod
    def _serialize(message: ChatMessage) -> Dict[str, Any]:
        """
        Serializes the SQLAlchemy ChatMessage model into a plain Python dictionary.
        """
        return {
            "id": str(message.id),
            "session_id": str(message.session_id),
            "role": message.role.value if hasattr(message.role, "value") else message.role,
            "message": message.message,
            "created_at": message.created_at.isoformat() if message.created_at else None,
        }
