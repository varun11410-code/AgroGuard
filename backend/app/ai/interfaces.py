"""
AgroGuard Backend - AI Interfaces

Defines the core interface contract for all AI providers within the system.
Any new provider must implement the AIProvider abstract base class to ensure
the service layer receives a consistent, predictable response format.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class AIProvider(ABC):
    """
    Abstract Base Class defining the contract for AgroGuard AI Providers.
    """
    
    @abstractmethod
    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Executes a prompt to generate a standard text response.
        
        Args:
            prompt: The user input or context string.
            system_instruction: Optional instructions for how the model should behave.
            
        Returns:
            The raw string response from the AI.
            
        Raises:
            AIProviderError: Base exception for general provider failures.
            AIProviderTimeout: If the provider takes too long to respond.
            AIProviderRateLimit: If the API quota is exhausted.
        """
        pass
        
    @abstractmethod
    def generate_structured_json(self, prompt: str, system_instruction: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes a prompt and guarantees a normalized JSON dictionary is returned.
        
        The provider implementation is strictly responsible for stripping any 
        vendor-specific markdown (e.g., ```json) and performing json.loads() 
        before returning the dictionary to the caller.
        
        Args:
            prompt: The input instructing the model to output JSON.
            system_instruction: Optional behavior instructions.
            
        Returns:
            A parsed Python dictionary representing the JSON response.
            
        Raises:
            AIProviderInvalidResponse: If the model output cannot be parsed as JSON.
            AIProviderError: Base exception for general provider failures.
        """
        pass
