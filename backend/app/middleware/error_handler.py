"""
AgroGuard Backend - Error Handlers

Centralized error handling for the application, formatting errors
from schemas (Pydantic), request parsing (Werkzeug), and application logic
(AgroGuardBaseException) into standard JSON contracts.
"""
from flask import Flask, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest
import logging

from app.core.exceptions import AgroGuardBaseException

logger = logging.getLogger(__name__)

def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(e: ValidationError):
        """
        Catches Pydantic schema validation errors globally and formats them.
        Returns a specific 'errors' array payload.
        """
        formatted_errors = []
        for err in e.errors():
            loc = err.get("loc", ("unknown",))
            field = str(loc[-1]) if loc else "unknown"
            formatted_errors.append({"field": field, "message": err.get("msg")})
            
        logger.info(f"Validation Error: {formatted_errors}")
        return jsonify({
            "success": False,
            "errors": formatted_errors
        }), 400

    @app.errorhandler(BadRequest)
    def handle_bad_request(e: BadRequest):
        """
        Catches JSON parsing failures.
        """
        logger.info("Bad Request: Missing or invalid JSON payload")
        return jsonify({
            "success": False,
            "message": "Missing or invalid JSON payload"
        }), 400

    from werkzeug.exceptions import RequestEntityTooLarge
    @app.errorhandler(RequestEntityTooLarge)
    def handle_entity_too_large(e: RequestEntityTooLarge):
        """
        Catches file uploads exceeding MAX_CONTENT_LENGTH.
        """
        logger.warning("Request Entity Too Large")
        return jsonify({
            "success": False,
            "message": "File exceeds maximum allowed size"
        }), 413

    @app.errorhandler(AgroGuardBaseException)
    def handle_agroguard_exception(e: AgroGuardBaseException):
        """
        Catches all custom application and domain logic exceptions.
        Formats them based on their defined HTTP status codes and enforces logging policy.
        """
        status_code = getattr(e, "status_code", 500)
        error_code = getattr(e, "error_code", None)
        log_msg = f"[{error_code}] {e.message}" if error_code else e.message

        if status_code == 400:
            logger.info(log_msg)
        elif status_code in (401, 403, 404, 409, 429):
            logger.warning(log_msg)
        else:
            # 5xx Expected Infrastructure Failures
            logger.error(log_msg, exc_info=True)

        return jsonify({
            "success": False,
            "message": e.message
        }), status_code

    from werkzeug.exceptions import HTTPException
    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        """
        Catches standard Werkzeug HTTP exceptions (e.g. 404 Not Found, 405 Method Not Allowed).
        Returns them as JSON with their proper status codes.
        """
        return jsonify({
            "success": False,
            "message": e.description
        }), e.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e: Exception):
        """
        Global Catch-All for any unexpected internal server errors.
        Prevents HTML tracebacks from leaking to the client in production or development,
        while securely capturing the full traceback server-side.
        """
        logger.critical("An unexpected internal server error occurred.", exc_info=True)
        
        from app.services.activity_log_service import ActivityLogService
        from flask import request
        from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
        import uuid
        
        user_id = None
        try:
            verify_jwt_in_request(optional=True)
            identity = get_jwt_identity()
            if identity:
                user_id = uuid.UUID(identity)
        except Exception:
            pass

        ActivityLogService.log_system_error(
            error_category=e.__class__.__name__,
            endpoint=request.path,
            request_method=request.method,
            user_id=user_id
        )
        return jsonify({
            "success": False,
            "message": "An unexpected internal server error occurred."
        }), 500
