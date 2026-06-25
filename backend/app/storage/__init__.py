"""
AgroGuard Backend - Storage Package

Provides a global storage provider instance initialized according to the 
Flask application factory pattern. 
"""

from app.storage.cloudinary import CloudinaryStorage

# Initialize the storage provider instance. 
# It will be bound to the Flask application in app/__init__.py via storage.init_app(app)
storage = CloudinaryStorage()

__all__ = ["storage"]
