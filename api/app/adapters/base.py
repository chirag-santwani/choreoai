from abc import ABC, abstractmethod
from typing import Dict, Any, AsyncIterator


class BaseAdapter(ABC):
    """
    Base adapter interface for AI provider integrations.
    All provider adapters must implement this interface.
    """

    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key
        self.config = kwargs

    @abstractmethod
    async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a chat completion.

        Args:
            request: Normalized request format

        Returns:
            Response in OpenAI-compatible format
        """
        pass

    @abstractmethod
    async def chat_completion_stream(self, request: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """
        Create a streaming chat completion.

        Args:
            request: Normalized request format

        Yields:
            Response chunks in OpenAI-compatible format
        """
        pass

    @abstractmethod
    async def create_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create embeddings.

        Args:
            request: Normalized request format

        Returns:
            Response in OpenAI-compatible format
        """
        pass

    @abstractmethod
    async def list_models(self) -> Dict[str, Any]:
        """
        List available models for this provider.

        Returns:
            List of models in OpenAI-compatible format
        """
        pass
