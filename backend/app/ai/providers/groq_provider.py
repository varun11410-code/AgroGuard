"""
AgroGuard Backend - Groq Provider

Implements the AIProvider interface for the Groq network.
Owns JSON normalization, network retries, and domain exception mapping.
"""
import json
import time
import logging
from typing import Dict, Any, Optional

try:
    import groq
    from groq import Groq
except ImportError:
    # If the SDK is not installed, we shouldn't crash the entire app unless this provider is explicitly requested.
    groq = None

from app.ai.interfaces import AIProvider
from app.ai.exceptions import (
    AIProviderError,
    AIProviderConfigurationError,
    AIProviderTimeout,
    AIProviderRateLimit,
    AIProviderInvalidResponse
)

logger = logging.getLogger(__name__)

class GroqProvider(AIProvider):
    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the Groq provider, failing fast if configuration is missing.
        """
        if not groq:
            raise AIProviderConfigurationError("The 'groq' python package is not installed.")

        self.api_key = config.get("GROQ_API_KEY")
        self.model = config.get("GROQ_MODEL")

        if not self.api_key:
            raise AIProviderConfigurationError("GROQ_API_KEY is missing from configuration.")
        if not self.model:
            raise AIProviderConfigurationError("GROQ_MODEL is missing from configuration.")

        try:
            self.client = Groq(api_key=self.api_key, timeout=10.0)
        except Exception as e:
            raise AIProviderConfigurationError(f"Failed to initialize Groq client: {str(e)}")

    def _execute_with_retry(self, messages: list, is_json: bool = False) -> str:
        """
        Executes a chat completion with a lightweight internal retry loop
        for transient network drops and timeouts.
        """
        max_attempts = 3
        backoff_seconds = 2

        for attempt in range(max_attempts):
            try:
                kwargs = {
                    "messages": messages,
                    "model": self.model,
                }
                if is_json:
                    kwargs["response_format"] = {"type": "json_object"}

                response = self.client.chat.completions.create(**kwargs)
                return response.choices[0].message.content

            except groq.AuthenticationError as e:
                # Non-retryable
                logger.error(f"Groq Authentication failed: {e}")
                raise AIProviderConfigurationError("Invalid Groq API Key.")
            except groq.RateLimitError as e:
                # Non-retryable (fail fast)
                logger.warning(f"Groq Rate limit exceeded: {e}")
                raise AIProviderRateLimit("Groq API quota exhausted.")
            except (groq.APITimeoutError, groq.APIConnectionError) as e:
                if attempt == max_attempts - 1:
                    logger.error(f"Groq connection/timeout failed after {max_attempts} attempts: {e}")
                    if isinstance(e, groq.APITimeoutError):
                        raise AIProviderTimeout("Groq API request timed out.")
                    else:
                        raise AIProviderError(f"Groq API connection failed: {e}")
                
                # Exponential backoff
                wait_time = backoff_seconds * (2 ** attempt)
                logger.info(f"Groq transient failure: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            except groq.APIError as e:
                # General API errors
                logger.error(f"Groq API Error: {e}")
                raise AIProviderError(f"Provider API failure: {e}")
            except Exception as e:
                logger.error(f"Unexpected Groq error: {e}", exc_info=True)
                raise AIProviderError(f"Unexpected provider error: {e}")

        raise AIProviderError("Execution failed after maximum retries.")

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        return self._execute_with_retry(messages, is_json=False)

    def generate_structured_json(self, prompt: str, system_instruction: Optional[str] = None) -> Dict[str, Any]:
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        raw_content = self._execute_with_retry(messages, is_json=True)

        # Normalize markdown if provider returns wrapped JSON
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
            logger.error(f"Failed to parse JSON from Groq: {e}\nRaw Content:\n{raw_content}")
            raise AIProviderInvalidResponse("Model output could not be parsed as JSON.")

        if not isinstance(parsed_data, dict):
            logger.error(f"Groq returned valid JSON, but root type is {type(parsed_data)}, expected dict.")
            raise AIProviderInvalidResponse("Model output parsed successfully, but root type is not a dictionary.")

        return parsed_data
