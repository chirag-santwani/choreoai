from typing import Dict, Any, AsyncIterator
from app.adapters.base import BaseAdapter
from anthropic import AsyncAnthropic
import time


class ClaudeAdapter(BaseAdapter):
    """
    Adapter for Anthropic Claude API.
    Converts between OpenAI-compatible format and Claude's API format.
    """

    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self.client = AsyncAnthropic(api_key=api_key)

    def _convert_messages_to_claude(self, messages: list) -> tuple[str, list]:
        """
        Convert OpenAI message format to Claude format.
        Returns (system_prompt, messages_list)
        """
        system_prompt = ""
        claude_messages = []

        for msg in messages:
            if msg["role"] == "system":
                # Claude uses a separate system parameter
                system_prompt = msg["content"]
            else:
                # Claude uses 'user' and 'assistant' roles like OpenAI
                claude_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        return system_prompt, claude_messages

    def _convert_claude_to_openai(self, claude_response, model: str) -> Dict[str, Any]:
        """Convert Claude response to OpenAI format."""
        return {
            "id": claude_response.id,
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": claude_response.content[0].text
                },
                "finish_reason": claude_response.stop_reason
            }],
            "usage": {
                "prompt_tokens": claude_response.usage.input_tokens,
                "completion_tokens": claude_response.usage.output_tokens,
                "total_tokens": claude_response.usage.input_tokens + claude_response.usage.output_tokens
            }
        }

    async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a chat completion using Claude API.
        """
        try:
            # Extract parameters
            model = request.get("model", "claude-3-sonnet-20240229")
            messages = request.get("messages", [])
            max_tokens = request.get("max_tokens", 1024)
            temperature = request.get("temperature", 1.0)

            # Convert messages
            system_prompt, claude_messages = self._convert_messages_to_claude(messages)

            # Call Claude API
            response = await self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt if system_prompt else None,
                messages=claude_messages
            )

            # Convert to OpenAI format
            return self._convert_claude_to_openai(response, model)

        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")

    async def chat_completion_stream(self, request: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """
        Create a streaming chat completion using Claude API.
        """
        try:
            # Extract parameters
            model = request.get("model", "claude-3-sonnet-20240229")
            messages = request.get("messages", [])
            max_tokens = request.get("max_tokens", 1024)
            temperature = request.get("temperature", 1.0)

            # Convert messages
            system_prompt, claude_messages = self._convert_messages_to_claude(messages)

            # Call Claude API with streaming
            async with self.client.messages.stream(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt if system_prompt else None,
                messages=claude_messages
            ) as stream:
                async for text in stream.text_stream:
                    # Convert each chunk to OpenAI format
                    chunk = {
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": model,
                        "choices": [{
                            "index": 0,
                            "delta": {
                                "content": text
                            },
                            "finish_reason": None
                        }]
                    }
                    yield chunk

        except Exception as e:
            raise Exception(f"Claude streaming error: {str(e)}")

    async def create_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create embeddings - not supported by Claude.
        """
        raise NotImplementedError("Claude does not support embeddings")

    async def list_models(self) -> Dict[str, Any]:
        """
        List available Claude models.
        """
        # Claude doesn't have a models API, so we return a static list
        return {
            "object": "list",
            "data": [
                {"id": "claude-3-5-sonnet-20241022", "object": "model", "owned_by": "anthropic", "created": 1729555200},
                {"id": "claude-3-5-sonnet-20240620", "object": "model", "owned_by": "anthropic", "created": 1718841600},
                {"id": "claude-3-opus-20240229", "object": "model", "owned_by": "anthropic", "created": 1709164800},
                {"id": "claude-3-sonnet-20240229", "object": "model", "owned_by": "anthropic", "created": 1709164800},
                {"id": "claude-3-haiku-20240307", "object": "model", "owned_by": "anthropic", "created": 1709769600},
                {"id": "claude-2.1", "object": "model", "owned_by": "anthropic", "created": 1700006400},
                {"id": "claude-2.0", "object": "model", "owned_by": "anthropic", "created": 1688169600},
            ]
        }
