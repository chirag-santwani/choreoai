from typing import Dict, Any, AsyncIterator
from app.adapters.base import BaseAdapter


class OpenAIAdapter(BaseAdapter):
    """
    Adapter for OpenAI API.
    """

    async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a chat completion using OpenAI API.
        """
        # TODO: Implement OpenAI chat completion
        raise NotImplementedError("OpenAI chat completion not yet implemented")

    async def chat_completion_stream(self, request: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """
        Create a streaming chat completion using OpenAI API.
        """
        # TODO: Implement OpenAI streaming chat completion
        raise NotImplementedError("OpenAI streaming not yet implemented")
        yield {}

    async def create_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create embeddings using OpenAI API.
        """
        # TODO: Implement OpenAI embeddings
        raise NotImplementedError("OpenAI embeddings not yet implemented")

    def list_models(self) -> Dict[str, Any]:
        """
        List available OpenAI models.
        """
        return {
            "object": "list",
            "data": [
                {"id": "gpt-4", "object": "model", "owned_by": "openai"},
                {"id": "gpt-4-turbo", "object": "model", "owned_by": "openai"},
                {"id": "gpt-3.5-turbo", "object": "model", "owned_by": "openai"},
            ]
        }
