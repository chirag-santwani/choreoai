from typing import Dict, Any, AsyncIterator
from app.adapters.base import BaseAdapter


class AzureAdapter(BaseAdapter):
    """
    Adapter for Azure OpenAI API.
    """

    def __init__(self, api_key: str, endpoint: str = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.endpoint = endpoint

    async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a chat completion using Azure OpenAI API.
        """
        # TODO: Implement Azure OpenAI chat completion
        raise NotImplementedError("Azure chat completion not yet implemented")

    async def chat_completion_stream(self, request: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """
        Create a streaming chat completion using Azure OpenAI API.
        """
        # TODO: Implement Azure OpenAI streaming chat completion
        raise NotImplementedError("Azure streaming not yet implemented")
        yield {}

    async def create_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create embeddings using Azure OpenAI API.
        """
        # TODO: Implement Azure OpenAI embeddings
        raise NotImplementedError("Azure embeddings not yet implemented")

    def list_models(self) -> Dict[str, Any]:
        """
        List available Azure OpenAI models.
        """
        return {
            "object": "list",
            "data": [
                {"id": "gpt-4", "object": "model", "owned_by": "azure-openai"},
                {"id": "gpt-35-turbo", "object": "model", "owned_by": "azure-openai"},
            ]
        }
