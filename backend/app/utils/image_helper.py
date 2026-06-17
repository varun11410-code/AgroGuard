"""
AgroGuard Backend - Image Helper Utilities

Utility functions for safely handling image operations, 
including fetching remote images from Cloudinary.
"""
import io
import requests
import logging

logger = logging.getLogger(__name__)

def fetch_image_to_buffer(url: str, timeout: int = 5) -> io.BytesIO | None:
    """
    Safely fetches a remote image (e.g., from Cloudinary) into a BytesIO stream.
    Returns None if the fetch fails, preventing network issues from crashing downstream tasks.
    
    Args:
        url (str): The URL of the image to fetch.
        timeout (int): Timeout in seconds for the network request.
        
    Returns:
        io.BytesIO | None: The byte stream of the image, or None if it could not be fetched.
    """
    if not url:
        return None
        
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        # Verify it's actually an image
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            logger.warning(f"URL did not return an image content type: {content_type}")
            return None
            
        return io.BytesIO(response.content)
        
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch image from {url}: {str(e)}")
        return None
