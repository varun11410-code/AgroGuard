import os
import uuid
from dotenv import load_dotenv
load_dotenv()
from app import create_app, db
from app.services.chat_orchestrator import ChatOrchestrator
from app.models.user import User

app = create_app()
with app.app_context():
    user = User.query.first()
    if not user:
        print("No users found in database.")
        exit(1)
    user_id = str(user.id)
    print("Testing Chatbot...")
    try:
        result = ChatOrchestrator.handle_chat_request(
            user_id=user_id, 
            message="How do I treat early blight?", 
            session_id=None, 
            scan_id=None, 
            selected_plan=None
        )
        print("Chatbot Response:")
        print(result["message"])
    except Exception as e:
        print(f"Chatbot Error: {e}")
