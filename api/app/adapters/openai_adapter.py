from typing import Dict, Any, AsyncIterator
from app.adapters.base import BaseAdapter
from openai import AsyncOpenAI
import json


class OpenAIAdapter(BaseAdapter):
    """
    Adapter for OpenAI API.
    """

    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self.client = AsyncOpenAI(api_key=api_key)

    async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a chat completion using OpenAI API.
        """
        try:
            response = await self.client.chat.completions.create(**request)
            return response.model_dump()
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def chat_completion_stream(self, request: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """
        Create a streaming chat completion using OpenAI API.
        """
        try:
            # Ensure stream is set to True (remove it from request if present)
            request_copy = request.copy()
            request_copy["stream"] = True

            stream = await self.client.chat.completions.create(**request_copy)
            async for chunk in stream:
                yield chunk.model_dump()
        except Exception as e:
            raise Exception(f"OpenAI streaming error: {str(e)}")

    async def create_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create embeddings using OpenAI API.
        """
        try:
            response = await self.client.embeddings.create(**request)
            return response.model_dump()
        except Exception as e:
            raise Exception(f"OpenAI embeddings error: {str(e)}")

    async def list_models(self) -> Dict[str, Any]:
        """
        List available OpenAI models from the API.
        """
        try:
            response = await self.client.models.list()
            return response.model_dump()
        except Exception as e:
            raise Exception(f"OpenAI list models error: {str(e)}")
