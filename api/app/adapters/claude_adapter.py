from typing import Dict, Any, AsyncIterator
from app.adapters.base import BaseAdapter


class ClaudeAdapter(BaseAdapter):
    """
    Adapter for Anthropic Claude API.
    """

    async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a chat completion using Claude API.
        """
        # TODO: Implement Claude chat completion
        raise NotImplementedError("Claude chat completion not yet implemented")

    async def chat_completion_stream(self, request: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """
        Create a streaming chat completion using Claude API.
        """
        # TODO: Implement Claude streaming chat completion
        raise NotImplementedError("Claude streaming not yet implemented")
        yield {}

    async def create_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create embeddings - not supported by Claude.
        """
        raise NotImplementedError("Claude does not support embeddings")

    def list_models(self) -> Dict[str, Any]:
        """
        List available Claude models.
        """
        return {
            "object": "list",
            "data": [
                {"id": "claude-3-opus-20240229", "object": "model", "owned_by": "anthropic"},
                {"id": "claude-3-sonnet-20240229", "object": "model", "owned_by": "anthropic"},
                {"id": "claude-3-haiku-20240307", "object": "model", "owned_by": "anthropic"},
            ]
        }
