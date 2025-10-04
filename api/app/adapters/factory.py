from app.adapters.base import BaseAdapter
from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.claude_adapter import ClaudeAdapter
from app.adapters.azure_adapter import AzureAdapter
from app.adapters.bedrock_adapter import BedrockAdapter
from app.adapters.gemini_adapter import GeminiAdapter
from app.adapters.grok_adapter import GrokAdapter
from app.config import settings


class AdapterFactory:
    """
    Factory class for creating provider adapters.
    """

    @staticmethod
    def get_adapter(provider: str) -> BaseAdapter:
        """
        Get the appropriate adapter for the given provider.

        Args:
            provider: Provider name (openai, claude, azure, bedrock, gemini, grok)

        Returns:
            Initialized adapter instance

        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        provider_lower = provider.lower()

        if provider_lower == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not configured")
            return OpenAIAdapter(api_key=settings.OPENAI_API_KEY)
        elif provider_lower == "claude":
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not configured")
            return ClaudeAdapter(api_key=settings.ANTHROPIC_API_KEY)
        elif provider_lower == "azure":
            if not settings.AZURE_OPENAI_API_KEY or not settings.AZURE_OPENAI_ENDPOINT:
                raise ValueError("Azure OpenAI credentials not configured")
            return AzureAdapter(
                api_key=settings.AZURE_OPENAI_API_KEY,
                endpoint=settings.AZURE_OPENAI_ENDPOINT
            )
        elif provider_lower == "bedrock":
            if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
                raise ValueError("AWS credentials not configured")
            return BedrockAdapter(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region=settings.AWS_REGION
            )
        elif provider_lower == "gemini":
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not configured")
            return GeminiAdapter(api_key=settings.GEMINI_API_KEY)
        elif provider_lower == "grok":
            if not settings.GROK_API_KEY:
                raise ValueError("GROK_API_KEY not configured")
            return GrokAdapter(api_key=settings.GROK_API_KEY)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @staticmethod
    def get_adapter_for_model(model: str) -> BaseAdapter:
        """
        Get the appropriate adapter based on the model name.

        Args:
            model: Model name (e.g., gpt-4, claude-3-opus, gemini-pro)

        Returns:
            Initialized adapter instance

        Raises:
            ValueError: If model is not recognized or supported
        """
        model_lower = model.lower()

        if model_lower.startswith("gpt-") or model_lower.startswith("o1-") or model_lower.startswith("text-embedding-"):
            return AdapterFactory.get_adapter("openai")
        elif model_lower.startswith("claude-"):
            return AdapterFactory.get_adapter("claude")
        elif model_lower.startswith("gemini-"):
            return AdapterFactory.get_adapter("gemini")
        elif model_lower.startswith("grok-"):
            return AdapterFactory.get_adapter("grok")
        else:
            raise ValueError(f"Unknown model: {model}. Model must start with a recognized provider prefix (gpt-, claude-, gemini-, grok-, etc.)")
