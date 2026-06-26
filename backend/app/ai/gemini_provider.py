"""
AgroGuard Backend - Gemini Provider

Migrated to implement the AIProvider interface for the Google Gemini network.
Owns JSON normalization, network execution, and domain exception mapping.
"""
import json
import logging
from typing import Dict, Any, Optional

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

from app.ai.interfaces import AIProvider
from app.ai.exceptions import (
    AIProviderError,
    AIProviderConfigurationError,
    AIProviderInvalidResponse
)

logger = logging.getLogger(__name__)

class GeminiProvider(AIProvider):
    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the Gemini provider, validating configuration.
        Note: The legacy setup relied on genai.configure() globally,
        but we now require it to be configured here or instantiated properly.
        """
        self.api_key = config.get("GEMINI_API_KEY")
        self.model_name = config.get("GEMINI_MODEL", "gemini-flash-latest")
        
        if not self.api_key:
            raise AIProviderConfigurationError("GEMINI_API_KEY is missing from configuration.")
            
        try:
            # We configure it here. If another provider uses this globally, 
            # it might conflict, but since we are migrating, this is standard.
            genai.configure(api_key=self.api_key)
        except Exception as e:
            raise AIProviderConfigurationError(f"Failed to configure Gemini client: {str(e)}")

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Standard text generation."""
        try:
            kwargs = {}
            if system_instruction:
                kwargs["system_instruction"] = system_instruction
                
            model = genai.GenerativeModel(model_name=self.model_name, **kwargs)
            response = model.generate_content(prompt)
            return response.text
            
        except ValueError as e:
            logger.error(f"Validation/Safety error from Gemini: {str(e)}")
            raise AIProviderError(f"AI generation blocked or invalid: {str(e)}")
        except GoogleAPIError as e:
            logger.error(f"Gemini API error: {str(e)}", exc_info=True)
            raise AIProviderError(f"Provider connection failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in GeminiProvider: {str(e)}", exc_info=True)
            raise AIProviderError(f"Unexpected error communicating with AI provider: {str(e)}")

    def generate_structured_json(self, prompt: str, system_instruction: Optional[str] = None) -> Dict[str, Any]:
        """Guarantees a dictionary response by normalizing markdown."""
        raw_content = self.generate_text(prompt, system_instruction)
        
        cleaned_content = raw_content.strip()
        if cleaned_content.startswith("```json"):
            cleaned_content = cleaned_content[7:]
        elif cleaned_content.startswith("```"):
            cleaned_content = cleaned_content[3:]
        
        if cleaned_content.endswith("```"):
            cleaned_content = cleaned_content[:-3]

        cleaned_content = cleaned_content.strip()

        try:
            parsed_data = json.loads(cleaned_content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Gemini: {e}\nRaw Content:\n{raw_content}")
            raise AIProviderInvalidResponse("Model output could not be parsed as JSON.")

        if not isinstance(parsed_data, dict):
            logger.error(f"Gemini returned valid JSON, but root type is {type(parsed_data)}, expected dict.")
            raise AIProviderInvalidResponse("Model output parsed successfully, but root type is not a dictionary.")

        return parsed_data
