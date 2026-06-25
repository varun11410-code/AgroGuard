"""
AgroGuard Backend - Storage Provider Abstraction

Defines the StorageProvider abstract base class to ensure the application
remains agnostic to the underlying storage provider (e.g. Cloudinary, S3).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class StorageUploadResult:
    """
    Data Transfer Object representing a successful storage upload.
    
    Attributes:
        url: The public, securely-accessible HTTPS URL of the uploaded file.
        provider_id: The unique identifier assigned or used by the provider
                     (e.g., Cloudinary public_id, S3 object key).
    """
    url: str
    provider_id: str

class StorageProvider(ABC):
    """
    Abstract Base Class for all storage implementations.
    """

    @abstractmethod
    def init_app(self, app) -> None:
        """
        Initialize the storage provider with the Flask application configuration.
        """
        pass

    @abstractmethod
    def upload_file(self, file_bytes: bytes, destination_path: str) -> StorageUploadResult:
        """
        Uploads a file to the storage provider.

        Args:
            file_bytes: The raw bytes of the file to upload.
            destination_path: The requested target path or identifier
                              (e.g., 'scans/1234-abcd.jpg').

        Returns:
            StorageUploadResult containing the URL and provider_id.

        Raises:
            StorageUploadError: If the upload operation fails.
            StorageConnectionError: If the provider is unreachable.
        """
        pass

    @abstractmethod
    def delete_file(self, destination_path: str) -> bool:
        """
        Deletes a file from the storage provider.

        Args:
            destination_path: The identifier or path of the file to delete
                              (must match the provider_id returned during upload).

        Returns:
            bool: True if deletion was successful.

        Raises:
            StorageDeleteError: If the deletion operation fails.
            StorageConnectionError: If the provider is unreachable.
        """
        pass
