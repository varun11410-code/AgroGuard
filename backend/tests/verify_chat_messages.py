import sys
import os
import uuid

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models.user import User, UserRole
from app.models.chat_message import MessageRole
from app.services.chat_session_service import ChatSessionService
from app.services.chat_message_service import ChatMessageService

def run_tests():
    app = create_app("testing")
    with app.app_context():
        # Setup schema
        db.create_all()

        # Users setup
        user1 = User(id=uuid.uuid4(), name="Test User 1", email="test1@test.com", password_hash="hash", role=UserRole.USER)
        user2 = User(id=uuid.uuid4(), name="Test User 2", email="test2@test.com", password_hash="hash", role=UserRole.USER)
        db.session.add_all([user1, user2])
        db.session.commit()

        u1_id = str(user1.id)
        u2_id = str(user2.id)

        # Create session
        session = ChatSessionService.create_session(u1_id)
        s_id = session["id"]

        print("--- Running ChatMessageService Tests ---")

        # Test 1: Create user message
        import time
        try:
            msg1 = ChatMessageService.save_message(s_id, u1_id, MessageRole.USER, "Hello AI")
            assert msg1["role"] == "USER"
            assert msg1["message"] == "Hello AI"
            print("Test 1 (Create user message): PASSED")
            time.sleep(1)
        except Exception as e:
            print(f"Test 1 FAILED: {str(e)}")

        # Test 2: Create assistant message
        try:
            msg2 = ChatMessageService.save_message(s_id, u1_id, MessageRole.ASSISTANT, "Hello User")
            assert msg2["role"] == "ASSISTANT"
            assert msg2["message"] == "Hello User"
            print("Test 2 (Create assistant message): PASSED")
            time.sleep(1)
        except Exception as e:
            print(f"Test 2 FAILED: {str(e)}")

        # Test 3: Retrieve session history
        try:
            history = ChatMessageService.get_session_history(s_id, u1_id)
            assert len(history) == 2
            assert history[0]["id"] == msg1["id"]
            assert history[1]["id"] == msg2["id"]
            print("Test 3 (Retrieve session history): PASSED")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Test 3 FAILED: {str(e)}")

        # Test 4: Message validation failure
        try:
            ChatMessageService.save_message(s_id, u1_id, MessageRole.USER, "   ")
            print("Test 4 FAILED: Expected ValueError for empty message")
        except ValueError:
            print("Test 4 (Message validation failure): PASSED")

        # Test 5: Unknown/Unauthorized session
        try:
            ChatMessageService.save_message(s_id, u2_id, MessageRole.USER, "Hack")
            print("Test 5 FAILED: Expected ValueError for unauthorized session")
        except ValueError:
            print("Test 5 (Unknown/Unauthorized session failure): PASSED")

        # Test 6: Multiple messages / Preserved ordering
        try:
            msg3 = ChatMessageService.save_message(s_id, u1_id, MessageRole.USER, "Third message")
            time.sleep(1)
            msg4 = ChatMessageService.save_message(s_id, u1_id, MessageRole.ASSISTANT, "Fourth message")
            history = ChatMessageService.get_session_history(s_id, u1_id)
            assert len(history) == 4
            assert history[-2]["id"] == msg3["id"]
            assert history[-1]["id"] == msg4["id"]
            print("Test 6 (Multiple messages ordering): PASSED")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Test 6 FAILED: {str(e)}")

        print("--- All Tests Completed ---")

if __name__ == "__main__":
    run_tests()
