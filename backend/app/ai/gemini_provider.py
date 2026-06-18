"""
AgroGuard Backend - Gemini Provider

Encapsulates direct communication with the Google Gemini API.
"""

import logging
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from app.utils.exceptions import AIProviderError

logger = logging.getLogger(__name__)

class GeminiProvider:
    @staticmethod
    def generate_text(
        prompt: str,
        system_instruction: str | None = None,
        model_name: str = "gemini-1.5-flash"
    ) -> str:
        """
        Sends a prompt to the Gemini API and returns the generated text.
        
        Args:
            prompt: The user input prompt.
            system_instruction: Optional system-level instructions.
            model_name: The Gemini model version to use.
            
        Returns:
            The raw string response from the AI.
            
        Raises:
            ValueError: If the prompt is empty.
            AIProviderError: If the Gemini SDK fails or returns an invalid response.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            kwargs = {}
            if system_instruction:
                kwargs["system_instruction"] = system_instruction
                
            model = genai.GenerativeModel(model_name=model_name, **kwargs)
            
            # Synchronous generation
            response = model.generate_content(prompt)
            
            return response.text

        except ValueError as e:
            # Handle cases where accessing response.text fails (e.g. blocked by safety settings)
            logger.error(f"Validation/Safety error from Gemini: {str(e)}")
            raise AIProviderError(f"AI generation blocked or invalid: {str(e)}")
        except GoogleAPIError as e:
            # Handle Google SDK specific exceptions
            logger.error(f"Gemini API error: {str(e)}", exc_info=True)
            raise AIProviderError(f"Provider connection failed: {str(e)}")
        except Exception as e:
            # Catch unexpected errors to prevent app crashes
            logger.error(f"Unexpected error in AI provider: {str(e)}", exc_info=True)
            raise AIProviderError("Unexpected error communicating with AI provider.")
