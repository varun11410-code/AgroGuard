"""
AgroGuard Backend - Error Handlers

Centralized error handling for the application, formatting errors
from schemas (Pydantic) and request parsing (Werkzeug) into standard JSON contracts.
"""
from flask import Flask, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(e: ValidationError):
        """
        Catches Pydantic schema validation errors globally and formats them
        exactly like the previous manual try-catch blocks.
        """
        formatted_errors = []
        for err in e.errors():
            loc = err.get("loc", ("unknown",))
            field = str(loc[-1]) if loc else "unknown"
            formatted_errors.append({"field": field, "message": err.get("msg")})
            
        return jsonify({
            "success": False,
            "errors": formatted_errors
        }), 400

    @app.errorhandler(BadRequest)
    def handle_bad_request(e: BadRequest):
        """
        Catches JSON parsing failures (when request.get_json() is called without silent=True).
        """
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
        return jsonify({
            "success": False,
            "message": "File exceeds maximum allowed size"
        }), 413

    @app.errorhandler(ValueError)
    def handle_value_error(e: ValueError):
        """
        Catches ValueError generally thrown by services.
        We check if it has a specific message to map to standard error codes.
        Note: Many controllers currently map specific ValueError strings to 401, 404, or 409.
        We leave this generic one here as a fallback, but controllers may still catch and handle 
        specific ValueErrors if they need specific HTTP status codes.
        """
        message = str(e)
        if message == "Invalid email or password":
            return jsonify({"success": False, "message": message}), 401
        elif message == "Email already exists":
            return jsonify({"success": False, "message": message}), 409
        elif message in ["User not found", "Scan not found", "Report not found"]:
            return jsonify({"success": False, "message": message}), 404
        elif message == "Access denied":
            return jsonify({"success": False, "message": message}), 403
            
        return jsonify({
            "success": False,
            "message": message
        }), 400
