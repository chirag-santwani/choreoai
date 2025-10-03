from typing import Dict, Any, AsyncIterator
from app.adapters.base import BaseAdapter


class GeminiAdapter(BaseAdapter):
    """
    Adapter for Google Gemini API.
    """

    async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a chat completion using Gemini API.
        """
        # TODO: Implement Gemini chat completion
        raise NotImplementedError("Gemini chat completion not yet implemented")

    async def chat_completion_stream(self, request: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """
        Create a streaming chat completion using Gemini API.
        """
        # TODO: Implement Gemini streaming chat completion
        raise NotImplementedError("Gemini streaming not yet implemented")
        yield {}

    async def create_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create embeddings using Gemini API.
        """
        # TODO: Implement Gemini embeddings
        raise NotImplementedError("Gemini embeddings not yet implemented")

    def list_models(self) -> Dict[str, Any]:
        """
        List available Gemini models.
        """
        return {
            "object": "list",
            "data": [
                {"id": "gemini-pro", "object": "model", "owned_by": "google"},
                {"id": "gemini-pro-vision", "object": "model", "owned_by": "google"},
            ]
        }
