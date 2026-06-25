"""
AgroGuard Backend - Cloudinary Storage Implementation

Implements the StorageProvider interface for Cloudinary.
Converts Cloudinary-specific exceptions into domain StorageError exceptions.
"""

import logging
import cloudinary
import cloudinary.uploader
import cloudinary.exceptions
from flask import Flask

from app.storage.provider import StorageProvider, StorageUploadResult
from app.storage.exceptions import (
    StorageConnectionError,
    StorageUploadError,
    StorageDeleteError,
)

logger = logging.getLogger(__name__)

class CloudinaryStorage(StorageProvider):
    """
    Cloudinary implementation of the StorageProvider.
    """

    def init_app(self, app: Flask) -> None:
        """
        Initialize Cloudinary with the Flask app configuration.
        Requires CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
        to be set in the app config.
        """
        cloud_name = app.config.get("CLOUDINARY_CLOUD_NAME")
        api_key = app.config.get("CLOUDINARY_API_KEY")
        api_secret = app.config.get("CLOUDINARY_API_SECRET")

        if not all([cloud_name, api_key, api_secret]):
            # Only warn, as local tests might not need valid credentials
            # until an actual upload is attempted.
            logger.warning("Cloudinary credentials are not fully configured in the environment.")

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True,
        )

    def upload_file(self, file_bytes: bytes, destination_path: str) -> StorageUploadResult:
        """
        Uploads a byte stream to Cloudinary.
        """
        try:
            # We pass the raw bytes. Cloudinary Python SDK accepts a string or a file-like object,
            # or bytes directly when using the uploader.
            response = cloudinary.uploader.upload(
                file_bytes,
                public_id=destination_path,
                resource_type="image"
            )
            
            return StorageUploadResult(
                url=response.get("secure_url"),
                provider_id=response.get("public_id")
            )

        except cloudinary.exceptions.Error as e:
            error_msg = str(e)
            logger.error(f"Cloudinary upload failed: {error_msg}")
            # Differentiate between connection/auth errors and standard upload errors
            if "Must supply api_key" in error_msg or "Invalid api_key" in error_msg:
                raise StorageConnectionError("Cloudinary authentication failed.") from e
            raise StorageUploadError(f"Upload failed: {error_msg}") from e
        except Exception as e:
            logger.error(f"Unexpected error during Cloudinary upload: {str(e)}")
            raise StorageUploadError("An unexpected error occurred during upload.") from e

    def delete_file(self, destination_path: str) -> bool:
        """
        Deletes a file from Cloudinary using its public_id.
        """
        try:
            response = cloudinary.uploader.destroy(
                public_id=destination_path,
                resource_type="image"
            )
            
            # Cloudinary returns 'result': 'ok' if deleted, or 'not found'
            if response.get("result") in ["ok", "not found"]:
                return True
                
            raise StorageDeleteError(f"Deletion returned unexpected result: {response.get('result')}")
            
        except cloudinary.exceptions.Error as e:
            error_msg = str(e)
            logger.error(f"Cloudinary deletion failed: {error_msg}")
            if "Must supply api_key" in error_msg or "Invalid api_key" in error_msg:
                raise StorageConnectionError("Cloudinary authentication failed.") from e
            raise StorageDeleteError(f"Deletion failed: {error_msg}") from e
        except Exception as e:
            logger.error(f"Unexpected error during Cloudinary deletion: {str(e)}")
            raise StorageDeleteError("An unexpected error occurred during deletion.") from e
