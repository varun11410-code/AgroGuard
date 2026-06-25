"""
AgroGuard Backend - Storage Exceptions

Defines the exception hierarchy for storage operations to prevent
leaking provider-specific errors (e.g., Cloudinary exceptions) into
the application domain logic.
"""

class StorageError(Exception):
    """Base exception for all storage operations."""
    pass

class StorageConnectionError(StorageError):
    """Raised when the storage provider cannot be reached or authentication fails."""
    pass

class StorageUploadError(StorageError):
    """Raised when an upload operation fails."""
    pass

class StorageDeleteError(StorageError):
    """Raised when a deletion operation fails."""
    pass
