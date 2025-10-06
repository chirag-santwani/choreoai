# Adding New Providers

This guide walks you through adding support for a new AI provider to ChoreoAI.

## Overview

Adding a new provider involves four main steps:

1. Create a new adapter class
2. Implement the required methods
3. Register the adapter in the factory
4. Add configuration settings
5. Test the implementation

## Step 1: Create the Adapter Class

### 1.1 Create the adapter file

Create a new file in `/api/app/adapters/` named after your provider:

```bash
touch api/app/adapters/my_provider_adapter.py
```

### 1.2 Import required dependencies

```python
from typing import Dict, Any, AsyncIterator
from app.adapters.base import BaseAdapter
import httpx
import time
```

### 1.3 Define the adapter class

```python
class MyProviderAdapter(BaseAdapter):
    """
    Adapter for My Provider API.
    Converts between OpenAI-compatible format and My Provider's API format.
    """

    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        # Initialize provider-specific client
        self.base_url = kwargs.get("base_url", "https://api.myprovider.com")
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )
```

## Step 2: Implement Required Methods

### 2.1 Implement `chat_completion`

This method handles non-streaming chat completions.

```python
async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a chat completion using My Provider API.

    Args:
        request: Normalized request in OpenAI format

    Returns:
        Response in OpenAI-compatible format

    Raises:
        Exception: If the API returns an error
    """
    try:
        # Extract parameters from OpenAI format
        model = request.get("model", "my-default-model")
        messages = request.get("messages", [])
        max_tokens = request.get("max_tokens", 1024)
        temperature = request.get("temperature", 1.0)

        # Convert messages to provider format
        provider_messages = self._convert_messages_to_provider(messages)

        # Call provider API
        response = await self.client.post(
            f"{self.base_url}/v1/completions",
            json={
                "model": model,
                "messages": provider_messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        )
        response.raise_for_status()
        provider_response = response.json()

        # Convert response to OpenAI format
        return self._convert_provider_to_openai(provider_response, model)

    except Exception as e:
        raise Exception(f"My Provider API error: {str(e)}")
```

### 2.2 Implement `chat_completion_stream`

This method handles streaming chat completions.

```python
async def chat_completion_stream(self, request: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
    """
    Create a streaming chat completion using My Provider API.

    Args:
        request: Normalized request in OpenAI format

    Yields:
        Response chunks in OpenAI-compatible format

    Raises:
        Exception: If the API returns an error
    """
    try:
        # Extract parameters
        model = request.get("model", "my-default-model")
        messages = request.get("messages", [])
        max_tokens = request.get("max_tokens", 1024)
        temperature = request.get("temperature", 1.0)

        # Convert messages
        provider_messages = self._convert_messages_to_provider(messages)

        # Call provider streaming API
        async with self.client.stream(
            "POST",
            f"{self.base_url}/v1/completions/stream",
            json={
                "model": model,
                "messages": provider_messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": True
            }
        ) as response:
            response.raise_for_status()

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]  # Remove "data: " prefix
                    if data == "[DONE]":
                        break

                    # Parse JSON chunk
                    chunk_data = json.loads(data)

                    # Convert to OpenAI format
                    openai_chunk = {
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": model,
                        "choices": [{
                            "index": 0,
                            "delta": {
                                "content": chunk_data.get("text", "")
                            },
                            "finish_reason": chunk_data.get("finish_reason")
                        }]
                    }
                    yield openai_chunk

    except Exception as e:
        raise Exception(f"My Provider streaming error: {str(e)}")
```

### 2.3 Implement `create_embedding`

This method handles embedding creation. If your provider doesn't support embeddings, raise `NotImplementedError`.

```python
async def create_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create embeddings using My Provider API.

    Args:
        request: Normalized request in OpenAI format

    Returns:
        Response in OpenAI-compatible format

    Raises:
        NotImplementedError: If provider doesn't support embeddings
        Exception: If the API returns an error
    """
    try:
        # Extract parameters
        model = request.get("model", "my-embedding-model")
        input_text = request.get("input")

        # Handle single string or list of strings
        if isinstance(input_text, str):
            input_text = [input_text]

        # Call provider API
        response = await self.client.post(
            f"{self.base_url}/v1/embeddings",
            json={
                "model": model,
                "input": input_text
            }
        )
        response.raise_for_status()
        provider_response = response.json()

        # Convert to OpenAI format
        return {
            "object": "list",
            "data": [
                {
                    "object": "embedding",
                    "index": i,
                    "embedding": emb
                }
                for i, emb in enumerate(provider_response["embeddings"])
            ],
            "model": model,
            "usage": {
                "prompt_tokens": provider_response.get("tokens_used", 0),
                "total_tokens": provider_response.get("tokens_used", 0)
            }
        }

    except Exception as e:
        raise Exception(f"My Provider embeddings error: {str(e)}")

# If not supported:
async def create_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
    """Create embeddings - not supported by My Provider."""
    raise NotImplementedError("My Provider does not support embeddings")
```

### 2.4 Implement `list_models`

This method returns available models. You can either query the provider's API or return a static list.

```python
async def list_models(self) -> Dict[str, Any]:
    """
    List available models for My Provider.

    Returns:
        List of models in OpenAI-compatible format
    """
    try:
        # Option 1: Query provider API
        response = await self.client.get(f"{self.base_url}/v1/models")
        response.raise_for_status()
        provider_models = response.json()

        # Convert to OpenAI format
        return {
            "object": "list",
            "data": [
                {
                    "id": model["id"],
                    "object": "model",
                    "owned_by": "my-provider",
                    "created": model.get("created", int(time.time()))
                }
                for model in provider_models["models"]
            ]
        }

    except Exception as e:
        # Option 2: Return static list if API doesn't support model listing
        return {
            "object": "list",
            "data": [
                {"id": "my-model-1", "object": "model", "owned_by": "my-provider", "created": 1700000000},
                {"id": "my-model-2", "object": "model", "owned_by": "my-provider", "created": 1700000000},
                {"id": "my-embedding-model", "object": "model", "owned_by": "my-provider", "created": 1700000000},
            ]
        }
```

## Step 3: Implement Helper Methods

### 3.1 Message format conversion

```python
def _convert_messages_to_provider(self, messages: list) -> list:
    """
    Convert OpenAI message format to provider format.

    Args:
        messages: Messages in OpenAI format

    Returns:
        Messages in provider format
    """
    provider_messages = []

    for msg in messages:
        # Example: Provider uses different role names
        role_mapping = {
            "system": "system_instruction",
            "user": "user_message",
            "assistant": "assistant_message"
        }

        provider_messages.append({
            "role": role_mapping.get(msg["role"], msg["role"]),
            "text": msg["content"]  # Provider uses "text" instead of "content"
        })

    return provider_messages
```

### 3.2 Response format conversion

```python
def _convert_provider_to_openai(self, provider_response: Dict[str, Any], model: str) -> Dict[str, Any]:
    """
    Convert provider response to OpenAI format.

    Args:
        provider_response: Response from provider API
        model: Model name

    Returns:
        Response in OpenAI-compatible format
    """
    return {
        "id": provider_response.get("id", f"chatcmpl-{int(time.time())}"),
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": provider_response["output"]["text"]
            },
            "finish_reason": provider_response.get("stop_reason", "stop")
        }],
        "usage": {
            "prompt_tokens": provider_response["usage"]["input_tokens"],
            "completion_tokens": provider_response["usage"]["output_tokens"],
            "total_tokens": provider_response["usage"]["total_tokens"]
        }
    }
```

## Step 4: Register the Adapter

### 4.1 Update the factory

Edit `/api/app/adapters/factory.py`:

```python
from app.adapters.my_provider_adapter import MyProviderAdapter

class AdapterFactory:
    @staticmethod
    def get_adapter(provider: str) -> BaseAdapter:
        """Get the appropriate adapter for the given provider."""
        provider_lower = provider.lower()

        # Add your provider
        if provider_lower == "myprovider":
            if not settings.MYPROVIDER_API_KEY:
                raise ValueError("MYPROVIDER_API_KEY not configured")
            return MyProviderAdapter(
                api_key=settings.MYPROVIDER_API_KEY,
                base_url=settings.MYPROVIDER_BASE_URL  # Optional
            )
        # ... existing providers ...

    @staticmethod
    def get_adapter_for_model(model: str) -> BaseAdapter:
        """Get the appropriate adapter based on the model name."""
        model_lower = model.lower()

        # Add model prefix detection
        if model_lower.startswith("mymodel-"):
            return AdapterFactory.get_adapter("myprovider")
        # ... existing model prefixes ...
```

### 4.2 Update adapter exports

Edit `/api/app/adapters/__init__.py`:

```python
from app.adapters.my_provider_adapter import MyProviderAdapter

__all__ = [
    "BaseAdapter",
    "OpenAIAdapter",
    "ClaudeAdapter",
    "MyProviderAdapter",  # Add your adapter
    # ... other adapters
]
```

## Step 5: Add Configuration

### 5.1 Update settings

Edit `/api/app/config.py`:

```python
class Settings(BaseSettings):
    # Existing settings...

    # My Provider Configuration
    MYPROVIDER_API_KEY: Optional[str] = None
    MYPROVIDER_BASE_URL: str = "https://api.myprovider.com"
```

### 5.2 Update environment example

Edit `/api/.env.example`:

```bash
# My Provider
MYPROVIDER_API_KEY=your-api-key-here
MYPROVIDER_BASE_URL=https://api.myprovider.com
```

## Step 6: Test Your Adapter

### 6.1 Create unit tests

Create `/api/tests/unit/test_my_provider_adapter.py`:

```python
import pytest
from unittest.mock import AsyncMock, patch
from app.adapters.my_provider_adapter import MyProviderAdapter

@pytest.mark.asyncio
async def test_chat_completion():
    """Test basic chat completion."""
    adapter = MyProviderAdapter(api_key="test-key")

    # Mock the HTTP client
    with patch.object(adapter.client, 'post') as mock_post:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "id": "test-id",
            "output": {"text": "Hello!"},
            "usage": {
                "input_tokens": 10,
                "output_tokens": 5,
                "total_tokens": 15
            }
        }
        mock_post.return_value = mock_response

        request = {
            "model": "my-model-1",
            "messages": [
                {"role": "user", "content": "Hi"}
            ]
        }

        response = await adapter.chat_completion(request)

        assert response["choices"][0]["message"]["content"] == "Hello!"
        assert response["usage"]["total_tokens"] == 15

@pytest.mark.asyncio
async def test_list_models():
    """Test model listing."""
    adapter = MyProviderAdapter(api_key="test-key")

    response = await adapter.list_models()

    assert response["object"] == "list"
    assert len(response["data"]) > 0
    assert all(model["owned_by"] == "my-provider" for model in response["data"])
```

### 6.2 Create integration tests

Create `/api/tests/integration/test_my_provider_flow.py`:

```python
import pytest
import os
from app.adapters.my_provider_adapter import MyProviderAdapter

@pytest.mark.skipif(
    not os.getenv("MYPROVIDER_API_KEY"),
    reason="MYPROVIDER_API_KEY not set"
)
@pytest.mark.asyncio
async def test_real_chat_completion():
    """Test with real API (requires API key)."""
    adapter = MyProviderAdapter(api_key=os.getenv("MYPROVIDER_API_KEY"))

    request = {
        "model": "my-model-1",
        "messages": [
            {"role": "user", "content": "Say 'test successful'"}
        ],
        "max_tokens": 50
    }

    response = await adapter.chat_completion(request)

    assert "choices" in response
    assert len(response["choices"]) > 0
    assert "message" in response["choices"][0]
    assert "content" in response["choices"][0]["message"]
```

### 6.3 Run the tests

```bash
# Run unit tests
cd api
pytest tests/unit/test_my_provider_adapter.py -v

# Run integration tests (requires API key)
export MYPROVIDER_API_KEY=your-key
pytest tests/integration/test_my_provider_flow.py -v
```

## Step 7: Manual Testing

### 7.1 Test with the API server

Start the server:
```bash
cd api
export MYPROVIDER_API_KEY=your-key
uvicorn app.main:app --reload
```

Test with curl:
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mymodel-1",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### 7.2 Test with the OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-myprovider-key",
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="mymodel-1",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

## Common Implementation Patterns

### Pattern 1: Separate System Messages

Some providers (like Claude) use a separate system parameter:

```python
def _convert_messages_to_provider(self, messages: list) -> tuple[str, list]:
    """Convert messages, extracting system prompt."""
    system_prompt = ""
    provider_messages = []

    for msg in messages:
        if msg["role"] == "system":
            system_prompt = msg["content"]
        else:
            provider_messages.append(msg)

    return system_prompt, provider_messages
```

### Pattern 2: SDK-Based Implementation

If the provider has an official SDK:

```python
from myprovider import AsyncMyProviderClient

class MyProviderAdapter(BaseAdapter):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self.client = AsyncMyProviderClient(api_key=api_key)

    async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Use SDK methods
        response = await self.client.chat.create(**request)
        return response.to_openai_format()
```

### Pattern 3: Custom Authentication

For providers with unique auth requirements:

```python
class MyProviderAdapter(BaseAdapter):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self.client_id = kwargs.get("client_id")
        self.client_secret = kwargs.get("client_secret")

    async def _get_access_token(self) -> str:
        """Get OAuth access token."""
        response = await httpx.post(
            "https://auth.myprovider.com/oauth/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials"
            }
        )
        return response.json()["access_token"]
```

## Best Practices

1. **Error Handling**: Always wrap API calls in try-except blocks and provide meaningful error messages
2. **Type Hints**: Use type hints for all parameters and return values
3. **Documentation**: Add docstrings to all methods
4. **Logging**: Add logging for debugging (use Python's `logging` module)
5. **Validation**: Validate input parameters before making API calls
6. **Rate Limiting**: Handle rate limit errors gracefully
7. **Retries**: Implement retry logic for transient failures
8. **Cleanup**: Close HTTP clients properly (use context managers or cleanup methods)

## Checklist

Before submitting your adapter:

- [ ] Adapter class inherits from `BaseAdapter`
- [ ] All abstract methods are implemented
- [ ] Message format conversion is correct
- [ ] Response format matches OpenAI structure
- [ ] Configuration settings added to `config.py`
- [ ] Adapter registered in `factory.py`
- [ ] Unit tests written and passing
- [ ] Integration tests written
- [ ] Manual testing completed
- [ ] Documentation updated
- [ ] Example script created (optional)
- [ ] Error handling implemented
- [ ] Code follows project style guidelines

## Next Steps

- Add an example script in `/examples` demonstrating your provider
- Update the main README to list your provider
- Update API documentation with provider-specific notes
- Consider adding provider-specific features (function calling, vision, etc.)

## Getting Help

If you need help adding a provider:
1. Review existing adapters (especially `claude_adapter.py`)
2. Check the [Project Structure](./project-structure.md) documentation
3. Open a discussion on GitHub
4. Reach out to the maintainers
