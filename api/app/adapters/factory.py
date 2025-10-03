from typing import Optional
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
    def get_adapter(provider: str) -> Optional[BaseAdapter]:
        """
        Get the appropriate adapter for the given provider.

        Args:
            provider: Provider name (openai, claude, azure, bedrock, gemini, grok)

        Returns:
            Initialized adapter instance
        """
        adapters = {
            "openai": lambda: OpenAIAdapter(api_key=settings.OPENAI_API_KEY),
            "claude": lambda: ClaudeAdapter(api_key=settings.ANTHROPIC_API_KEY),
            "azure": lambda: AzureAdapter(
                api_key=settings.AZURE_OPENAI_API_KEY,
                endpoint=settings.AZURE_OPENAI_ENDPOINT
            ),
            "bedrock": lambda: BedrockAdapter(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region=settings.AWS_REGION
            ),
            "gemini": lambda: GeminiAdapter(api_key=settings.GEMINI_API_KEY),
            "grok": lambda: GrokAdapter(api_key=settings.GROK_API_KEY),
        }

        adapter_creator = adapters.get(provider.lower())
        if adapter_creator:
            return adapter_creator()
        return None

    @staticmethod
    def get_adapter_for_model(model: str) -> Optional[BaseAdapter]:
        """
        Get the appropriate adapter based on the model name.

        Args:
            model: Model name (e.g., gpt-4, claude-3-opus, gemini-pro)

        Returns:
            Initialized adapter instance
        """
        model_lower = model.lower()

        if model_lower.startswith("gpt-"):
            return AdapterFactory.get_adapter("openai")
        elif model_lower.startswith("claude-"):
            return AdapterFactory.get_adapter("claude")
        elif model_lower.startswith("gemini-"):
            return AdapterFactory.get_adapter("gemini")
        elif model_lower.startswith("grok-"):
            return AdapterFactory.get_adapter("grok")
        else:
            return None
