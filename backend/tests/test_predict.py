import os
import sys
import traceback
import uuid
from io import BytesIO

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from app import create_app
from app.database import db
from app.models.user import User
from app.models.crop import Crop
from app.services.scan_service import ScanService

def run_controller_test():
    app = create_app()
    with app.app_context():
        # Get user
        test_user = db.session.query(User).first()
        test_crop = db.session.query(Crop).first()
        
        tiny_gif = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        
        print("Executing exact prediction logic...")
        try:
            ScanService.save_scan(
                user_id=str(test_user.id),
                crop_name=test_crop.name,
                disease="Late Blight",
                confidence=0.88,
                image_bytes=tiny_gif
            )
            print("Successfully persisted")
        except Exception as e:
            print("EXCEPTION CAUGHT!")
            traceback.print_exc()

if __name__ == "__main__":
    run_controller_test()
