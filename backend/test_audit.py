import os
import sys
import traceback
import uuid
from io import BytesIO

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from app import create_app
from app.database import db
from app.models.user import User
from app.models.crop import Crop
from app.services.scan_service import ScanService
from app.storage import storage
from app.storage.exceptions import StorageError
from app.repositories.scan_repository import ScanRepository

def run_audit():
    app = create_app()
    with app.app_context():
        print("Starting Forensic Audit...")
        
        # 1. Setup test data
        test_user = db.session.query(User).first()
        if not test_user:
            # Create a mock user
            test_user = User(
                id=uuid.uuid4(),
                email="audit@test.com",
                password_hash="mock",
                first_name="Audit",
                last_name="User"
            )
            db.session.add(test_user)
            db.session.commit()
            
        test_crop = db.session.query(Crop).first()
        if not test_crop:
            print("No crop found, cannot proceed.")
            return

        print(f"Using User: {test_user.id}")
        print(f"Using Crop: {test_crop.name}")

        # Tiny valid GIF
        tiny_gif = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

        try:
            ScanService.save_scan(
                user_id=str(test_user.id),
                crop_name=test_crop.name,
                disease="Test Disease",
                confidence=0.99,
                image_bytes=tiny_gif
            )
            print("SUCCESS: Scan persisted successfully.")
        except Exception as e:
            print("\nEXCEPTION CAUGHT DURING SAVE_SCAN:")
            traceback.print_exc()

if __name__ == "__main__":
    run_audit()
