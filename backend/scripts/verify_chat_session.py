import sys
import os
import uuid

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models.user import User, UserRole
from app.models.scan import Scan
from app.models.chat_session import ChatSession
from app.services.chat_session_service import ChatSessionService

def run_tests():
    app = create_app("testing")
    with app.app_context():
        # Setup: Create DB schema in memory
        db.create_all()

        # Create dummy users
        user1 = User(id=uuid.uuid4(), name="Test User 1", email="test1@test.com", password_hash="hash", role=UserRole.USER)
        user2 = User(id=uuid.uuid4(), name="Test User 2", email="test2@test.com", password_hash="hash", role=UserRole.USER)
        db.session.add_all([user1, user2])
        db.session.commit()

        u1_id = str(user1.id)
        u2_id = str(user2.id)

        print("--- Running Tests ---")

        # Test 1: Create Mode A session
        try:
            session_a = ChatSessionService.create_session(u1_id)
            assert session_a["user_id"] == u1_id
            assert session_a["scan_id"] is None
            print("Test 1 (Create Mode A): PASSED")
        except Exception as e:
            print(f"Test 1 FAILED: {str(e)}")

        # Test 2: Create Mode B session (requires a dummy scan)
        try:
            from app.models.crop import Crop
            crop1 = Crop(id=uuid.uuid4(), name="Tomato", supported=True)
            db.session.add(crop1)
            
            scan1 = Scan(id=uuid.uuid4(), user_id=user1.id, crop_id=crop1.id, image_url="http://test.com/img.jpg")
            db.session.add(scan1)
            db.session.commit()
            
            s1_id = str(scan1.id)
            session_b = ChatSessionService.create_session(u1_id, scan_id=s1_id)
            assert session_b["user_id"] == u1_id
            assert session_b["scan_id"] == s1_id
            print("Test 2 (Create Mode B): PASSED")
        except Exception as e:
            print(f"Test 2 FAILED: {str(e)}")

        # Test 3: Get session success (ownership validation)
        try:
            retrieved = ChatSessionService.get_session(session_a["id"], u1_id)
            assert retrieved["id"] == session_a["id"]
            print("Test 3 (Get Session Owned): PASSED")
        except Exception as e:
            print(f"Test 3 FAILED: {str(e)}")

        # Test 4: Get session failure (unauthorized / wrong owner)
        try:
            ChatSessionService.get_session(session_a["id"], u2_id)
            print("Test 4 FAILED: Expected ValueError, got success")
        except ValueError as e:
            print(f"Test 4 (Get Session Unauthorized): PASSED (Caught expected ValueError)")
        except Exception as e:
            print(f"Test 4 FAILED: Unexpected exception {type(e)}")

        # Test 5: Get user sessions
        try:
            u1_sessions = ChatSessionService.get_user_sessions(u1_id)
            assert len(u1_sessions) == 2
            u2_sessions = ChatSessionService.get_user_sessions(u2_id)
            assert len(u2_sessions) == 0
            print("Test 5 (Get User Sessions): PASSED")
        except Exception as e:
            print(f"Test 5 FAILED: {str(e)}")

        print("--- All Tests Completed ---")

if __name__ == "__main__":
    run_tests()
