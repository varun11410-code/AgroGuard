"""
AgroGuard Backend - Auth Routes

Maps URLs to AuthController methods.
"""
from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    return AuthController.register()
