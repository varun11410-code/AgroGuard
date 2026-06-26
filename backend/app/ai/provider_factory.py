"""
AgroGuard Backend - AI Provider Factory

Centralized registry and resolution mechanism for AI providers.
Ensures the application adheres to the Open/Closed Principle when
new providers are added.

To add a new provider:
1. Implement the AIProvider interface.
2. Register the provider in the _REGISTRY below.
3. Configure the environment variable AI_PROVIDER to select it.
"""
from typing import Dict, Type, Any
from app.ai.interfaces import AIProvider
from app.ai.exceptions import AIProviderConfigurationError
from app.ai.providers.groq_provider import GroqProvider

class AIProviderFactory:
    """
    Factory for instantiating the correct AIProvider based on configuration.
    """
    
    # Centralized registry mapping configuration strings to provider classes
    _REGISTRY: Dict[str, Type[AIProvider]] = {
        "groq": GroqProvider
    }
    
    @classmethod
    def register_provider(cls, name: str, provider_cls: Type[AIProvider]) -> None:
        """Registers a provider class under a specific string name."""
        cls._REGISTRY[name.lower()] = provider_cls

    @classmethod
    def get_provider(cls, config: Dict[str, Any]) -> AIProvider:
        """
        Resolves and instantiates the active provider based on the provided configuration dictionary.
        
        Args:
            config: The application configuration dictionary containing AI_PROVIDER 
                    and any requisite API keys.
                    
        Returns:
            An instantiated AIProvider ready for execution.
            
        Raises:
            AIProviderConfigurationError: If the requested provider is unsupported or missing.
        """
        provider_name = config.get("AI_PROVIDER")
        if not provider_name:
            raise AIProviderConfigurationError("AI_PROVIDER is not set in the configuration.")
            
        provider_name = provider_name.lower()
        provider_cls = cls._REGISTRY.get(provider_name)
        
        if not provider_cls:
            raise AIProviderConfigurationError(
                f"Unsupported AI provider: '{provider_name}'. "
                f"Must be one of {list(cls._REGISTRY.keys())}"
            )
            
        # The provider class itself will handle validating its own specific 
        # required config keys (like GROQ_API_KEY) during __init__.
        try:
            return provider_cls(config)
        except Exception as e:
             raise AIProviderConfigurationError(f"Failed to initialize AI provider '{provider_name}': {str(e)}")
