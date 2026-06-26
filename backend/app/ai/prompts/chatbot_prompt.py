"""
AgroGuard Backend - Chatbot Prompts

Defines prompt generation functions for the conversational agricultural assistant.
Pure text generation only. No SDKs or network calls.
"""
from typing import Dict, Any, Optional

def build_chatbot_system_instruction(context_dict: Dict[str, Any]) -> str:
    """
    Constructs the system instruction giving the AI context about the 
    user's current diagnosis session.
    """
    selected_plan = context_dict.get('selected_plan') or 'None'
    
    return (
        f"You are an agricultural AI assistant. The user is asking about a crop diagnosis.\n"
        f"Crop: {context_dict['crop']}\n"
        f"Disease: {context_dict['disease']}\n"
        f"Confidence: {context_dict['confidence']:.2f}\n"
        f"Selected Plan: {selected_plan}\n"
        f"Provide brief, helpful advice related to this context."
    )
