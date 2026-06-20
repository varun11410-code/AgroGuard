"""
AgroGuard Backend - Auth Controller

Handles request-response lifecycle for authentication endpoints.
"""
import logging
from flask import request, jsonify
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError
from flask_jwt_extended import get_jwt_identity, get_jwt

from app.schemas.auth_schema import RegisterRequestSchema, LoginRequestSchema
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

    @staticmethod
    def login():
        """
        Handle POST /api/auth/login
        """
        try:
            data = request.get_json(silent=True)
            if not data or not isinstance(data, dict):
                return jsonify({"success": False, "message": "Missing or invalid JSON payload"}), 400

            validated_data = LoginRequestSchema(**data)

            response_data = AuthService.login_user(
                email=validated_data.email,
                password=validated_data.password
            )

            return jsonify(response_data), 200

        except ValidationError as e:
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
            if str(e) == "Invalid email or password":
                return jsonify({
                    "success": False,
                    "message": "Invalid email or password"
                }), 401
            
            return jsonify({
                "success": False,
                "message": str(e)
            }), 400

        except HTTPException as e:
            raise e

        except Exception as e:
            logging.exception("Unexpected error in login endpoint:")
            return jsonify({
                "success": False,
                "message": "An unexpected server error occurred"
            }), 500

    @staticmethod
    def refresh():
        """
        Handle POST /api/auth/refresh
        """
        try:
            identity = get_jwt_identity()
            claims = get_jwt()

            access_token = AuthService.refresh_access_token(
                identity=identity,
                claims=claims
            )

            return jsonify({
                "success": True,
                "data": {
                    "access_token": access_token
                }
            }), 200

        except Exception as e:
            logging.exception("Unexpected error in refresh endpoint:")
            return jsonify({
                "success": False,
                "message": "An unexpected server error occurred"
            }), 500

    @staticmethod
    def me():
        """
        Handle GET /api/auth/me
        """
        try:
            identity = get_jwt_identity()

            user_data = AuthService.get_current_user(user_id=identity)

            return jsonify({
                "success": True,
                "data": user_data
            }), 200

        except ValueError as e:
            if str(e) == "User not found":
                return jsonify({
                    "success": False,
                    "message": "User not found"
                }), 404
            
            return jsonify({
                "success": False,
                "message": str(e)
            }), 400

        except Exception as e:
            logging.exception("Unexpected error in me endpoint:")
            return jsonify({
                "success": False,
                "message": "An unexpected server error occurred"
            }), 500

    @staticmethod
    def preferences():
        """
        Handle PATCH /api/auth/preferences
        """
        try:
            identity = get_jwt_identity()
            data = request.get_json(silent=True)
            if not data or not isinstance(data, dict):
                return jsonify({"success": False, "message": "Missing or invalid JSON payload"}), 400

            from app.schemas.auth_schema import UpdatePreferencesSchema
            validated_data = UpdatePreferencesSchema(**data)

            user_data = AuthService.update_preferences(
                user_id=identity,
                language=validated_data.language,
                preferred_budget_tier=validated_data.preferred_budget_tier
            )

            return jsonify({
                "success": True,
                "data": user_data
            }), 200

        except ValidationError as e:
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
            if str(e) == "User not found":
                return jsonify({
                    "success": False,
                    "message": "User not found"
                }), 404
            
            return jsonify({
                "success": False,
                "message": str(e)
            }), 400

        except HTTPException as e:
            raise e

        except Exception as e:
            import logging
            logging.exception("Unexpected error in preferences endpoint:")
            return jsonify({
                "success": False,
                "message": "An unexpected server error occurred"
            }), 500

    @staticmethod
    def admin_test():
        """
        Handle GET /api/auth/admin-test
        Demonstration endpoint for verifying RBAC.
        """
        return jsonify({
            "success": True,
            "message": "Admin access granted"
        }), 200

    @staticmethod
    def logout():
        """
        Handle POST /api/auth/logout
        """
        try:
            claims = get_jwt()
            jti = claims["jti"]
            expires_at = claims["exp"]

            AuthService.logout_user(jti=jti, expires_at=expires_at)

            return jsonify({
                "success": True,
                "message": "Successfully logged out"
            }), 200

        except Exception as e:
            import logging
            logging.exception("Unexpected error in logout endpoint:")
            return jsonify({
                "success": False,
                "message": "An unexpected server error occurred"
            }), 500
