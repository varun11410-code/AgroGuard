"""
AgroGuard Backend - Chat Routes

Exposes API endpoints for chat orchestration and history.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from app.schemas.chat_schema import ChatRequestSchema
from app.services.chat_orchestrator import ChatOrchestrator
from app.services.chat_session_service import ChatSessionService
from app.services.chat_message_service import ChatMessageService
import logging

logger = logging.getLogger(__name__)

chat_bp = Blueprint("chat", __name__)

@chat_bp.post("/chat")
@jwt_required()
def send_message():
    """
    POST /api/chat
    Processes an incoming user message, queries Gemini, and saves both messages.
    """
    user_id = get_jwt_identity()
    
    try:
        data = request.get_json() or {}

        validated_data = ChatRequestSchema(**data)
        
        result = ChatOrchestrator.handle_chat_request(
            user_id=user_id,
            message=validated_data.message,
            session_id=validated_data.session_id,
            scan_id=validated_data.scan_id,
            selected_plan=validated_data.selected_plan
        )
        
        return jsonify({
            "success": True,
            "session_id": result["session_id"],
            "message": result["message"]
        }), 200


    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except HTTPException as e:
        return jsonify({"success": False, "message": e.description}), e.code
    except Exception as e:
        logger.exception("Unexpected error in chat orchestrator")
        return jsonify({"success": False, "message": "An unexpected server error occurred."}), 500


@chat_bp.get("/chat/session")
@jwt_required()
def get_session_history():
    """
    GET /api/chat/session
    Fetches history for a session. If scan_id is provided, fetches the specific session for that scan.
    Otherwise fetches the most recent general session.
    """
    user_id = get_jwt_identity()
    from app.schemas.common_schema import ChatSessionQuerySchema
    query_data = ChatSessionQuerySchema(**request.args.to_dict())
    scan_id = query_data.scan_id

    try:
        sessions = ChatSessionService.get_user_sessions(user_id)
        
        target_session = None
        if scan_id:
            target_session = next((s for s in sessions if s.get("scan_id") == scan_id), None)
        else:
            # Get the most recent general session (scan_id is None)
            general_sessions = [s for s in sessions if not s.get("scan_id")]
            if general_sessions:
                target_session = sorted(general_sessions, key=lambda x: x["created_at"], reverse=True)[0]
        
        if not target_session:
            return jsonify({"success": True, "session": None, "history": []}), 200

        history = ChatMessageService.get_session_history(target_session["id"], user_id)
        
        return jsonify({
            "success": True,
            "session": target_session,
            "history": history
        }), 200

    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logger.exception("Unexpected error fetching chat history")
        return jsonify({"success": False, "message": "An unexpected server error occurred."}), 500
