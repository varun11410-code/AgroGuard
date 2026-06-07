"""
AgroGuard Backend - Auth Routes

Maps URLs to AuthController methods.
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    return AuthController.register()

@auth_bp.post("/login")
def login():
    return AuthController.login()

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    return AuthController.refresh()
