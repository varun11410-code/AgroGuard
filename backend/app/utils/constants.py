"""
AgroGuard Backend - Constants

Defines centralized configuration rules for security, validation, and extensibility.
"""

# Upload Security Config
ALLOWED_UPLOAD_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

# Dimension Limits (Security)
MAX_PIXELS = 16_777_216  # 4096 * 4096 = 16.7 MP max

# Magic Numbers (File Signatures)
MAGIC_NUMBERS = {
    "jpeg": [b"\xFF\xD8\xFF"],
    "png": [b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"]
}
