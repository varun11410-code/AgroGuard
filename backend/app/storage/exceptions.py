"""
AgroGuard Backend - Storage Exceptions

Defines the exception hierarchy for storage operations to prevent
leaking provider-specific errors (e.g., Cloudinary exceptions) into
the application domain logic.

(These are now centralized in app.core.exceptions)
"""

from app.core.exceptions import (
    StorageError,
    StorageConnectionError,
    StorageUploadError,
    StorageDeleteError,
)
