"""
AgroGuard Backend - Auth Controller

Handles request-response lifecycle for authentication endpoints.
"""
import logging
from flask import request, jsonify
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError

from app.schemas.auth_schema import RegisterRequestSchema
from app.services.auth_service import AuthService

class AuthController:
    @staticmethod
    def register():
        """
        Handle POST /api/auth/register
        """
        try:
            # 1. Parse JSON payload (silent=True prevents Flask from automatically raising BadRequest)
            data = request.get_json(silent=True)
            if not data or not isinstance(data, dict):
                return jsonify({"success": False, "message": "Missing or invalid JSON payload"}), 400

            # 2. Validate using Pydantic
            validated_data = RegisterRequestSchema(**data)

            # 3. Call Service layer
            user_data = AuthService.register_user(
                name=validated_data.name,
                email=validated_data.email,
                password=validated_data.password
            )

            # 4. Return success response (201 Created)
            return jsonify({
                "success": True,
                "data": user_data
            }), 201

        except ValidationError as e:
            # Return 400 Validation errors with specific field messages
            formatted_errors = []
            for err in e.errors():
                loc = err.get("loc", ("unknown",))
                field = str(loc[-1]) if loc else "unknown"
                formatted_errors.append({"field": field, "message": err.get("msg")})
                
            return jsonify({
                "success": False,
                "errors": formatted_errors
            }), 400

        except ValueError as e:
            # Return 409 Conflict if email exists
            if str(e) == "Email already exists":
                return jsonify({
                    "success": False,
                    "message": str(e)
                }), 409
            
            return jsonify({
                "success": False,
                "message": str(e)
            }), 400

        except HTTPException as e:
            # Re-raise standard Flask HTTP exceptions (e.g., 404, 405) so they aren't caught as 500s
            raise e

        except Exception as e:
            # Log the full traceback to the server console for debugging
            logging.exception("Unexpected error in register endpoint:")
            
            # Return 500 Unexpected server errors
            # Never expose internal implementation details in 500 per AI_AGENT_RULES
            return jsonify({
                "success": False,
                "message": "An unexpected server error occurred"
            }), 500
