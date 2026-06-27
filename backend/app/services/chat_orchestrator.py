"""
AgroGuard Backend - Chat Orchestrator

Coordinates the complex sequence of session creation, context injection,
AI execution, and message persistence without acting as a God-Service.
"""
import logging
from typing import Dict, Any, Optional
from flask import current_app
from werkzeug.exceptions import ServiceUnavailable

from app.services.chat_session_service import ChatSessionService
from app.services.chat_message_service import ChatMessageService
from app.models.chat_message import MessageRole
from app.ai.provider_factory import AIProviderFactory
from app.ai.prompts.chatbot_prompt import build_chatbot_system_instruction
from app.ai.context_builder import ContextBuilder
from app.ai.exceptions import AIProviderError

logger = logging.getLogger(__name__)

class ChatOrchestrator:
    @staticmethod
    def handle_chat_request(user_id: str, message: str, session_id: Optional[str] = None, scan_id: Optional[str] = None, selected_plan: Optional[str] = None) -> Dict[str, Any]:
        """
        Orchestrates the chat message lifecycle.
        
        Flow:
        1. Auto-create session if none exists.
        2. Validate ownership.
        3. Persist user message to prevent data loss on AI timeout.
        4. Construct disease context prompt (if scan_id exists).
        5. Query AI provider.
        6. Persist assistant message.
        7. Return response.
        """
        # 1. Lazy Session Creation
        if not session_id:
            try:
                session_dict = ChatSessionService.create_session(user_id=user_id, scan_id=scan_id)
                session_id = session_dict["id"]
            except Exception as e:
                logger.error(f"Failed to create session: {e}", exc_info=True)
                raise

        # 2. Persist User Message FIRST (guarantees no data loss if AI fails)
        try:
            ChatMessageService.save_message(
                session_id=session_id,
                user_id=user_id,
                role=MessageRole.USER,
                message=message
            )
        except Exception as e:
            logger.error(f"Failed to save user message: {e}", exc_info=True)
            raise

        # 3. Context Injection (Mode B only)
        system_instruction = None
        if scan_id:
            try:
                # We need to fetch the scan to pass to the ContextBuilder
                from app.models.scan import Scan
                scan = Scan.query.filter_by(id=scan_id, user_id=user_id).first()
                if scan:
                    context_dict = ContextBuilder.build_disease_context(scan, selected_plan)
                    system_instruction = build_chatbot_system_instruction(context_dict)
            except Exception as e:
                # We log but do not fail the chat if context injection fails
                logger.warning(f"Failed to build disease context: {e}", exc_info=True)

        # 4. Fetch History for Context
        try:
            history = ChatMessageService.get_session_history(session_id, user_id)
            # Build a prompt that includes previous history
            # We append history text manually for compatibility with standard prompt signatures
            history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['message']}" for msg in history[-10:]]) # Limit history
            full_prompt = f"{history_text}\nAssistant:" if history else message
        except Exception as e:
            logger.error(f"Failed to fetch history for AI prompt: {e}", exc_info=True)
            raise

        # 5. Execute AI Call
        try:
            provider = AIProviderFactory.get_provider(current_app.config)
            ai_response_text = provider.generate_text(
                prompt=full_prompt,
                system_instruction=system_instruction
            )
        except AIProviderError as e:
            # AI failed. User message is safe. We abort before saving a broken AI message.
            # We raise ServiceUnavailable to preserve legacy HTTP behavior.
            raise ServiceUnavailable(description=str(e))
        except Exception as e:
            logger.error(f"Unexpected AI failure: {e}", exc_info=True)
            raise ServiceUnavailable(description="AI Provider is temporarily unavailable.")

        from app.services.activity_log_service import ActivityLogService
        import uuid
        uid_obj = None
        if user_id:
            try:
                uid_obj = uuid.UUID(user_id)
            except ValueError:
                pass
        ActivityLogService.log_ai_interaction(
            user_id=uid_obj,
            session_id=uuid.UUID(session_id),
            provider=current_app.config.get("AI_PROVIDER", "groq"),
            interaction_type="chat",
            scan_id=uuid.UUID(scan_id) if scan_id else None
        )

        # 6. Persist Assistant Response
        try:
            ai_message_dict = ChatMessageService.save_message(
                session_id=session_id,
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                message=ai_response_text
            )
        except Exception as e:
            logger.error(f"Failed to save assistant message: {e}", exc_info=True)
            raise

        # 7. Return Result
        return {
            "session_id": session_id,
            "message": ai_message_dict
        }
