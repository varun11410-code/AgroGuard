"""
AgroGuard Backend - Configuration Module

Provides environment-based configuration classes for Flask.

Classes:
    Config: Base configuration with shared settings.
    DevelopmentConfig: Local development settings.
    TestingConfig: In-memory SQLite for unit tests.
    ProductionConfig: Hardened production settings.

Usage:
    from app.config import config_map
    app.config.from_object(config_map[env])
"""

import os
from datetime import timedelta


class Config:
    """Base configuration shared across all environments."""

    # Flask
    SECRET_KEY: str = os.getenv("SECRET_KEY") or "change-me-in-production"

    # SQLAlchemy — falls back to local SQLite when DATABASE_URL is unset or blank
    SQLALCHEMY_DATABASE_URI: str = (
        os.getenv("DATABASE_URL") or "sqlite:///agroguard_dev.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # JWT — falls back to a safe dev default when JWT_SECRET_KEY is unset or blank
    JWT_SECRET_KEY: str = (
        os.getenv("JWT_SECRET_KEY") or "jwt-change-me-in-production"
    )
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=24)
    JWT_ALGORITHM: str = "HS256"

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


class DevelopmentConfig(Config):
    """Development configuration — debug enabled."""

    DEBUG: bool = True
    TESTING: bool = False


class TestingConfig(Config):
    """Testing configuration — uses in-memory SQLite."""

    DEBUG: bool = True
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(minutes=5)


class ProductionConfig(Config):
    """Production configuration — debug disabled, strict settings."""

    DEBUG: bool = False
    TESTING: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 10,
        "max_overflow": 20,
    }


# Map environment name strings to config classes
config_map: dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
