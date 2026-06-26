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
from app.ai.gemini_provider import GeminiProvider

class AIProviderFactory:
    """
    Factory for instantiating and caching the active AIProvider based on configuration.
    """
    
    # Centralized registry mapping configuration strings to provider classes
    _REGISTRY: Dict[str, Type[AIProvider]] = {
        "groq": GroqProvider,
        "gemini": GeminiProvider
    }
    
    # Cache mapping provider names to instantiated, stateful provider singletons
    _instances: Dict[str, AIProvider] = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_cls: Type[AIProvider]) -> None:
        """Registers a provider class under a specific string name."""
        cls._REGISTRY[name.lower()] = provider_cls

    @classmethod
    def get_provider(cls, config: Dict[str, Any]) -> AIProvider:
        """
        Resolves, instantiates (or retrieves from cache), and returns the active provider.
        
        Args:
            config: The application configuration dictionary containing AI_PROVIDER 
                    and any requisite API keys.
                    
        Returns:
            An AIProvider instance ready for execution.
            
        Raises:
            AIProviderConfigurationError: If the requested provider is unsupported or missing.
        """
        provider_name = config.get("AI_PROVIDER")
        if not provider_name:
            raise AIProviderConfigurationError("AI_PROVIDER is not set in the configuration.")
            
        provider_name = provider_name.lower()
        
        # Check cache first for efficiency
        if provider_name in cls._instances:
            return cls._instances[provider_name]
            
        provider_cls = cls._REGISTRY.get(provider_name)
        
        if not provider_cls:
            raise AIProviderConfigurationError(
                f"Unsupported AI provider: '{provider_name}'. "
                f"Must be one of {list(cls._REGISTRY.keys())}"
            )
            
        # The provider class itself handles validating its own specific config keys
        try:
            instance = provider_cls(config)
            cls._instances[provider_name] = instance
            return instance
        except Exception as e:
             raise AIProviderConfigurationError(f"Failed to initialize AI provider '{provider_name}': {str(e)}")
