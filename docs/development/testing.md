# Testing Guide

This guide covers testing practices, tools, and guidelines for ChoreoAI development.

## Overview

ChoreoAI uses **pytest** as the primary testing framework with support for:
- Unit tests
- Integration tests
- Asynchronous testing
- Mocking and fixtures
- Code coverage reporting

## Test Structure

```
choreoai/
├── api/
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py           # Shared fixtures
│       ├── unit/
│       │   ├── test_adapters.py
│       │   ├── test_routers.py
│       │   ├── test_factory.py
│       │   └── test_utils.py
│       └── integration/
│           ├── test_openai_flow.py
│           ├── test_claude_flow.py
│           └── test_streaming.py
│
└── client/
    └── tests/
        ├── __init__.py
        ├── conftest.py
        ├── test_client.py
        ├── test_chat_resource.py
        └── test_embeddings_resource.py
```

## Setting Up Testing Environment

### Install Testing Dependencies

```bash
# API testing dependencies
cd api
pip install pytest pytest-asyncio pytest-cov pytest-mock httpx

# Client testing dependencies
cd ../client
pip install pytest pytest-asyncio pytest-cov
```

### Configure pytest

Create or update `pytest.ini` in the project root:

```ini
[pytest]
testpaths = api/tests client/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow-running tests
    requires_api_key: Tests requiring real API keys
```

## Writing Unit Tests

Unit tests verify individual components in isolation using mocks.

### Example: Testing an Adapter

```python
# api/tests/unit/test_adapters.py

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.adapters.openai_adapter import OpenAIAdapter

@pytest.fixture
def openai_adapter():
    """Create an OpenAI adapter for testing."""
    return OpenAIAdapter(api_key="test-key")

@pytest.mark.asyncio
async def test_chat_completion_success(openai_adapter):
    """Test successful chat completion."""
    # Mock the OpenAI client response
    mock_response = MagicMock()
    mock_response.model_dump.return_value = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-3.5-turbo",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello! How can I help you?"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 8,
            "total_tokens": 18
        }
    }

    # Patch the client's method
    with patch.object(
        openai_adapter.client.chat.completions,
        'create',
        return_value=mock_response
    ):
        request = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "Hello"}
            ]
        }

        response = await openai_adapter.chat_completion(request)

        assert response["id"] == "chatcmpl-123"
        assert response["choices"][0]["message"]["content"] == "Hello! How can I help you?"
        assert response["usage"]["total_tokens"] == 18

@pytest.mark.asyncio
async def test_chat_completion_error(openai_adapter):
    """Test chat completion error handling."""
    with patch.object(
        openai_adapter.client.chat.completions,
        'create',
        side_effect=Exception("API Error")
    ):
        request = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello"}]
        }

        with pytest.raises(Exception) as exc_info:
            await openai_adapter.chat_completion(request)

        assert "OpenAI API error" in str(exc_info.value)
```

### Example: Testing the Factory

```python
# api/tests/unit/test_factory.py

import pytest
from app.adapters.factory import AdapterFactory
from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.claude_adapter import ClaudeAdapter
from unittest.mock import patch

def test_get_adapter_for_openai():
    """Test getting OpenAI adapter by provider name."""
    with patch('app.config.settings.OPENAI_API_KEY', 'test-key'):
        adapter = AdapterFactory.get_adapter("openai")
        assert isinstance(adapter, OpenAIAdapter)

def test_get_adapter_for_claude():
    """Test getting Claude adapter by provider name."""
    with patch('app.config.settings.ANTHROPIC_API_KEY', 'test-key'):
        adapter = AdapterFactory.get_adapter("claude")
        assert isinstance(adapter, ClaudeAdapter)

def test_get_adapter_missing_key():
    """Test error when API key is missing."""
    with patch('app.config.settings.OPENAI_API_KEY', None):
        with pytest.raises(ValueError, match="OPENAI_API_KEY not configured"):
            AdapterFactory.get_adapter("openai")

def test_get_adapter_for_model_gpt():
    """Test getting adapter by GPT model name."""
    with patch('app.config.settings.OPENAI_API_KEY', 'test-key'):
        adapter = AdapterFactory.get_adapter_for_model("gpt-4")
        assert isinstance(adapter, OpenAIAdapter)

def test_get_adapter_for_model_claude():
    """Test getting adapter by Claude model name."""
    with patch('app.config.settings.ANTHROPIC_API_KEY', 'test-key'):
        adapter = AdapterFactory.get_adapter_for_model("claude-3-opus-20240229")
        assert isinstance(adapter, ClaudeAdapter)

def test_get_adapter_unknown_model():
    """Test error for unknown model."""
    with pytest.raises(ValueError, match="Unknown model"):
        AdapterFactory.get_adapter_for_model("unknown-model-123")
```

### Example: Testing Routers

```python
# api/tests/unit/test_routers.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "ChoreoAI" in response.json()["service"]

@patch('app.routers.chat.AdapterFactory.get_adapter_for_model')
def test_chat_completion_endpoint(mock_get_adapter):
    """Test chat completion endpoint."""
    # Mock adapter
    mock_adapter = AsyncMock()
    mock_adapter.chat_completion.return_value = {
        "id": "test-id",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "gpt-3.5-turbo",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": "Test response"},
            "finish_reason": "stop"
        }],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
    }
    mock_get_adapter.return_value = mock_adapter

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Test"}]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["choices"][0]["message"]["content"] == "Test response"
```

## Writing Integration Tests

Integration tests verify the complete flow with real or mock external services.

### Example: Testing Complete Flow

```python
# api/tests/integration/test_openai_flow.py

import pytest
import os
from app.adapters.openai_adapter import OpenAIAdapter

@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set"
)
@pytest.mark.asyncio
async def test_openai_chat_completion_real():
    """Test with real OpenAI API."""
    adapter = OpenAIAdapter(api_key=os.getenv("OPENAI_API_KEY"))

    request = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say 'test'"}
        ],
        "max_tokens": 10
    }

    response = await adapter.chat_completion(request)

    assert "choices" in response
    assert len(response["choices"]) > 0
    assert "message" in response["choices"][0]
    assert "usage" in response
    assert response["usage"]["total_tokens"] > 0

@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set"
)
@pytest.mark.asyncio
async def test_openai_streaming_real():
    """Test streaming with real OpenAI API."""
    adapter = OpenAIAdapter(api_key=os.getenv("OPENAI_API_KEY"))

    request = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Count to 3"}
        ],
        "max_tokens": 50,
        "stream": True
    }

    chunks = []
    async for chunk in adapter.chat_completion_stream(request):
        chunks.append(chunk)

    assert len(chunks) > 0
    assert all(chunk["object"] == "chat.completion.chunk" for chunk in chunks)
```

## Shared Fixtures

Use `conftest.py` to define shared fixtures:

```python
# api/tests/conftest.py

import pytest
from unittest.mock import MagicMock
from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.claude_adapter import ClaudeAdapter

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client."""
    client = MagicMock()
    return client

@pytest.fixture
def openai_adapter():
    """OpenAI adapter with test key."""
    return OpenAIAdapter(api_key="test-openai-key")

@pytest.fixture
def claude_adapter():
    """Claude adapter with test key."""
    return ClaudeAdapter(api_key="test-claude-key")

@pytest.fixture
def sample_messages():
    """Sample messages for testing."""
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]

@pytest.fixture
def sample_openai_response():
    """Sample OpenAI API response."""
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-3.5-turbo",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello! How can I help you?"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 8,
            "total_tokens": 28
        }
    }
```

## Running Tests

### Run All Tests

```bash
# From project root
pytest

# From specific directory
cd api
pytest tests/
```

### Run Specific Test Types

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Exclude slow tests
pytest -m "not slow"

# Tests requiring API keys
pytest -m requires_api_key
```

### Run Specific Test Files

```bash
# Single file
pytest api/tests/unit/test_adapters.py

# Specific test function
pytest api/tests/unit/test_adapters.py::test_chat_completion_success

# Pattern matching
pytest -k "chat_completion"
```

### Run with Coverage

```bash
# Generate coverage report
pytest --cov=app --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

### Run with Verbose Output

```bash
# Show all test names
pytest -v

# Show print statements
pytest -s

# Both verbose and print
pytest -vs
```

## Test Coverage Requirements

Target coverage levels:
- **Overall**: 80%+
- **Adapters**: 90%+
- **Routers**: 85%+
- **Utils**: 90%+

Check coverage:
```bash
pytest --cov=app --cov-report=term-missing
```

## Testing Async Code

### Basic Async Test

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await some_async_function()
    assert result == expected_value
```

### Testing Async Generators

```python
@pytest.mark.asyncio
async def test_streaming():
    """Test async generator."""
    chunks = []
    async for chunk in async_generator():
        chunks.append(chunk)

    assert len(chunks) > 0
```

### Async Fixtures

```python
@pytest.fixture
async def async_client():
    """Async fixture."""
    client = AsyncClient()
    await client.connect()
    yield client
    await client.disconnect()

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    """Use async fixture."""
    result = await async_client.query()
    assert result is not None
```

## Mocking Best Practices

### Mock External API Calls

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_with_mock():
    """Test with mocked external call."""
    with patch('httpx.AsyncClient.post') as mock_post:
        mock_response = AsyncMock()
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response

        result = await function_that_calls_api()
        assert result["result"] == "success"
```

### Mock Configuration

```python
from unittest.mock import patch

def test_with_config_mock():
    """Test with mocked configuration."""
    with patch('app.config.settings.OPENAI_API_KEY', 'test-key'):
        # Test code that uses settings
        pass
```

### Mock Multiple Objects

```python
from unittest.mock import patch

def test_multiple_mocks():
    """Test with multiple mocks."""
    with patch('app.adapters.openai_adapter.AsyncOpenAI') as mock_openai, \
         patch('app.config.settings.OPENAI_API_KEY', 'test-key'):
        # Test code
        pass
```

## Parameterized Tests

Test multiple scenarios with one test function:

```python
@pytest.mark.parametrize("model,expected_provider", [
    ("gpt-4", "openai"),
    ("gpt-3.5-turbo", "openai"),
    ("claude-3-opus-20240229", "claude"),
    ("claude-3-sonnet-20240229", "claude"),
    ("gemini-pro", "gemini"),
])
def test_model_to_provider(model, expected_provider):
    """Test model name to provider mapping."""
    provider = get_provider_from_model(model)
    assert provider == expected_provider
```

## Testing Error Handling

```python
@pytest.mark.asyncio
async def test_api_error_handling(openai_adapter):
    """Test handling of API errors."""
    with patch.object(
        openai_adapter.client.chat.completions,
        'create',
        side_effect=Exception("API Error")
    ):
        with pytest.raises(Exception) as exc_info:
            await openai_adapter.chat_completion({"messages": []})

        assert "API Error" in str(exc_info.value)

def test_validation_error():
    """Test input validation."""
    with pytest.raises(ValueError, match="Invalid model"):
        validate_model("invalid-model-name")
```

## Testing Streaming Responses

```python
@pytest.mark.asyncio
async def test_stream_processing():
    """Test streaming response processing."""
    async def mock_stream():
        """Mock streaming generator."""
        for i in range(5):
            yield {"delta": {"content": f"chunk{i}"}}

    chunks = []
    async for chunk in mock_stream():
        chunks.append(chunk)

    assert len(chunks) == 5
    assert chunks[0]["delta"]["content"] == "chunk0"
```

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        cd api
        pip install -r requirements.txt
        pip install pytest pytest-asyncio pytest-cov

    - name: Run tests
      run: |
        cd api
        pytest tests/ --cov=app --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Test Organization Best Practices

1. **One test per behavior**: Each test should verify one specific behavior
2. **Clear test names**: Use descriptive names that explain what's being tested
3. **AAA pattern**: Arrange, Act, Assert
4. **Independent tests**: Tests should not depend on each other
5. **Clean fixtures**: Use fixtures for common setup
6. **Mock external dependencies**: Don't make real API calls in unit tests
7. **Test edge cases**: Include tests for error conditions and edge cases

## Example Test Structure

```python
@pytest.mark.asyncio
async def test_feature_name_scenario():
    """Test description explaining what's being verified."""
    # Arrange - Set up test data and mocks
    adapter = OpenAIAdapter(api_key="test-key")
    request = {"model": "gpt-4", "messages": []}

    mock_response = create_mock_response()
    with patch.object(adapter.client, 'create', return_value=mock_response):
        # Act - Execute the code being tested
        result = await adapter.chat_completion(request)

        # Assert - Verify the results
        assert result["id"] == "expected-id"
        assert result["choices"][0]["message"]["content"] == "expected-content"
```

## Debugging Failed Tests

### Show Print Output

```bash
pytest -s
```

### Stop on First Failure

```bash
pytest -x
```

### Enter Debugger on Failure

```bash
pytest --pdb
```

### Run Last Failed Tests

```bash
pytest --lf
```

## Next Steps

- Write tests for new features before implementing them (TDD)
- Aim for high coverage on critical paths
- Run tests before committing code
- Review test results in CI/CD pipeline
- Update tests when refactoring code

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [Python unittest.mock guide](https://docs.python.org/3/library/unittest.mock.html)
