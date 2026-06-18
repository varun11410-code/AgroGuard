"""
AgroGuard Backend - AI Setup Module

Configures the Google Gemini SDK at application startup.
"""

import google.generativeai as genai
from flask import Flask


def setup_gemini(app: Flask) -> None:
    """
    Configures the Gemini SDK using the API key from Flask config.
    This should be called once during application startup.
    """
    api_key = app.config.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
