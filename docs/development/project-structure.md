# Project Structure

This document explains the organization and structure of the ChoreoAI codebase.

## Repository Layout

```
choreoai/
├── api/                    # FastAPI backend service
│   ├── app/
│   │   ├── adapters/      # Provider-specific adapters
│   │   ├── middleware/    # Authentication, logging, rate limiting
│   │   ├── routers/       # API route handlers
│   │   ├── schemas/       # Pydantic models for requests/responses
│   │   ├── utils/         # Utility functions
│   │   ├── config.py      # Application configuration
│   │   └── main.py        # FastAPI application entry point
│   ├── tests/             # API tests
│   │   ├── unit/          # Unit tests
│   │   └── integration/   # Integration tests
│   ├── Dockerfile         # API service Docker image
│   └── requirements.txt   # Python dependencies
│
├── client/                # Python client library
│   ├── choreoai/
│   │   ├── resources/     # Resource-specific clients
│   │   │   ├── chat.py
│   │   │   └── embeddings.py
│   │   ├── types/         # Type definitions
│   │   ├── client.py      # Main client class
│   │   └── exceptions.py  # Custom exceptions
│   ├── tests/             # Client tests
│   ├── pyproject.toml     # Package metadata
│   └── setup.py           # Package setup
│
├── docs/                  # Documentation
│   ├── api/               # API documentation
│   ├── client/            # Client library documentation
│   ├── deployment/        # Deployment guides
│   └── development/       # Development guides (this section)
│
├── examples/              # Example scripts and use cases
│   ├── basic_usage.py
│   ├── list_models.py
│   ├── function_calling.py
│   ├── cost_optimization.py
│   ├── ab_testing.py
│   └── embeddings_rag.py
│
├── infrastructure/        # Infrastructure as Code
│   ├── docker/            # Docker configurations
│   ├── helm/              # Helm charts for Kubernetes
│   ├── kubernetes/        # Raw Kubernetes manifests
│   └── terraform/         # Terraform configurations
│
├── scripts/               # Utility scripts
│   ├── deploy.sh
│   ├── setup_dev.sh
│   └── test.sh
│
├── docker-compose.yml     # Docker Compose configuration
├── Makefile               # Common development commands
├── README.md              # Project overview
└── .gitignore             # Git ignore rules
```

## API Service (`/api`)

The API service is built with FastAPI and provides a unified OpenAI-compatible interface.

### Core Modules

#### `app/main.py`
- FastAPI application initialization
- CORS configuration
- Router registration
- Health check endpoints

```python
from fastapi import FastAPI
from app.routers import chat, embeddings, models

app = FastAPI(title="ChoreoAI")
app.include_router(chat.router, prefix="/v1", tags=["chat"])
app.include_router(embeddings.router, prefix="/v1", tags=["embeddings"])
app.include_router(models.router, prefix="/v1", tags=["models"])
```

#### `app/config.py`
- Environment variable management
- Configuration settings using Pydantic
- API key validation

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    # ... other settings

    class Config:
        env_file = ".env"
```

### Adapters (`app/adapters/`)

Adapters implement the provider-specific logic to translate between OpenAI format and each provider's native format.

**Key Files:**
- `base.py` - Abstract base class defining the adapter interface
- `factory.py` - Factory pattern for creating adapters
- `openai_adapter.py` - OpenAI implementation
- `claude_adapter.py` - Anthropic Claude implementation
- `gemini_adapter.py` - Google Gemini implementation
- `grok_adapter.py` - xAI Grok implementation
- `azure_adapter.py` - Azure OpenAI implementation
- `bedrock_adapter.py` - AWS Bedrock implementation

**Base Adapter Interface:**
```python
class BaseAdapter(ABC):
    @abstractmethod
    async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Create a chat completion."""
        pass

    @abstractmethod
    async def chat_completion_stream(self, request: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """Create a streaming chat completion."""
        pass

    @abstractmethod
    async def create_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Create embeddings."""
        pass

    @abstractmethod
    async def list_models(self) -> Dict[str, Any]:
        """List available models."""
        pass
```

### Routers (`app/routers/`)

Route handlers for API endpoints.

- `chat.py` - Chat completion endpoints (`/v1/chat/completions`)
- `embeddings.py` - Embeddings endpoints (`/v1/embeddings`)
- `models.py` - Model listing endpoints (`/v1/models`)

**Example Router:**
```python
from fastapi import APIRouter, Request
from app.adapters.factory import AdapterFactory

router = APIRouter()

@router.post("/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    adapter = AdapterFactory.get_adapter_for_model(request.model)

    if request.stream:
        return StreamingResponse(
            adapter.chat_completion_stream(request.dict())
        )
    else:
        return await adapter.chat_completion(request.dict())
```

### Schemas (`app/schemas/`)

Pydantic models for request/response validation.

- `requests.py` - Request models (ChatCompletionRequest, EmbeddingRequest)
- `responses.py` - Response models (ChatCompletionResponse, ErrorResponse)

### Middleware (`app/middleware/`)

- `auth.py` - API key authentication
- `logging.py` - Request/response logging
- `rate_limit.py` - Rate limiting logic

### Utils (`app/utils/`)

- `errors.py` - Custom exception classes
- `retry.py` - Retry logic for external API calls

## Client Library (`/client`)

Python SDK for interacting with ChoreoAI.

### Structure

```
client/choreoai/
├── __init__.py           # Package exports
├── client.py             # Main ChoreoAI client
├── exceptions.py         # Custom exceptions
├── resources/
│   ├── __init__.py
│   ├── chat.py          # Chat resource
│   └── embeddings.py    # Embeddings resource
└── types/
    ├── __init__.py
    └── chat_completion.py  # Type definitions
```

### Main Client (`client.py`)

```python
class ChoreoAI:
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url
        self.chat = ChatResource(self)
        self.embeddings = EmbeddingsResource(self)
```

### Resources

Resources encapsulate specific API functionality:

```python
class ChatResource:
    def __init__(self, client: ChoreoAI):
        self.client = client

    async def create(self, **kwargs) -> ChatCompletion:
        """Create a chat completion."""
        response = await self.client._request(
            "POST", "/v1/chat/completions", json=kwargs
        )
        return ChatCompletion(**response)
```

## Examples (`/examples`)

Example scripts demonstrating various use cases:

- `basic_usage.py` - Simple chat completions
- `list_models.py` - Listing available models
- `function_calling.py` - Using function calling
- `cost_optimization.py` - Cost-aware model selection
- `ab_testing.py` - A/B testing different models
- `embeddings_rag.py` - Embeddings and RAG patterns

Each example is self-contained and includes:
- Detailed comments
- Error handling
- Multiple provider examples
- Output formatting

## Infrastructure (`/infrastructure`)

### Docker (`infrastructure/docker/`)

Docker configurations for different deployment scenarios.

### Kubernetes (`infrastructure/kubernetes/`)

Kubernetes manifests:
- `deployment.yaml` - API deployment
- `service.yaml` - Service definition
- `ingress.yaml` - Ingress rules
- `configmap.yaml` - Configuration
- `secret.yaml.example` - Secret template

### Helm (`infrastructure/helm/`)

Helm chart for Kubernetes deployment:
```
helm/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    └── configmap.yaml
```

### Terraform (`infrastructure/terraform/`)

Infrastructure as Code for cloud resources:
- AWS configurations
- Azure configurations
- GCP configurations

## Tests

### API Tests (`/api/tests`)

```
tests/
├── unit/
│   ├── test_adapters.py
│   ├── test_routers.py
│   └── test_utils.py
└── integration/
    ├── test_openai_flow.py
    ├── test_claude_flow.py
    └── test_streaming.py
```

### Client Tests (`/client/tests`)

```
tests/
├── test_client.py
├── test_chat_resource.py
├── test_embeddings_resource.py
└── test_exceptions.py
```

## File Naming Conventions

- **Python files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/methods**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Test files**: `test_*.py`
- **Config files**: `lowercase` or `kebab-case`

## Module Organization Principles

### Single Responsibility
Each module has a single, well-defined purpose:
- Adapters handle provider-specific logic
- Routers handle HTTP request/response
- Schemas handle data validation
- Utils provide reusable functions

### Dependency Direction
Dependencies flow in one direction:
```
Routers → Adapters → External APIs
   ↓
Schemas
   ↓
Utils
```

### Interface Segregation
Adapters implement only the methods they support:
```python
# Claude doesn't support embeddings
async def create_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError("Claude does not support embeddings")
```

## Key Architectural Patterns

### Factory Pattern
`AdapterFactory` creates the appropriate adapter based on model or provider:
```python
adapter = AdapterFactory.get_adapter_for_model("gpt-4")
adapter = AdapterFactory.get_adapter("openai")
```

### Adapter Pattern
Each provider adapter converts between OpenAI format and provider format:
```python
class ClaudeAdapter(BaseAdapter):
    def _convert_messages_to_claude(self, messages: list) -> tuple[str, list]:
        # Convert OpenAI format to Claude format
        ...

    def _convert_claude_to_openai(self, response, model: str) -> Dict[str, Any]:
        # Convert Claude response to OpenAI format
        ...
```

### Strategy Pattern
Different authentication strategies for different providers:
- API key in header (OpenAI, Anthropic)
- Endpoint + key (Azure)
- AWS credentials (Bedrock)

### Dependency Injection
Configuration and dependencies injected via constructor:
```python
class OpenAIAdapter(BaseAdapter):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self.client = AsyncOpenAI(api_key=api_key)
```

## Configuration Management

### Environment Variables
All configuration via environment variables:
- Development: `.env` file
- Production: System environment or secret manager

### Settings Validation
Pydantic validates and type-checks all settings:
```python
class Settings(BaseSettings):
    PORT: int = 8000  # Default with type checking
    OPENAI_API_KEY: Optional[str] = None  # Optional
```

### Multi-Environment Support
Different configurations for different environments:
- `ENVIRONMENT=development` - Local development
- `ENVIRONMENT=staging` - Staging environment
- `ENVIRONMENT=production` - Production

## Import Conventions

### Absolute Imports
Always use absolute imports:
```python
from app.adapters.base import BaseAdapter
from app.config import settings
```

### Avoid Circular Imports
Structure modules to avoid circular dependencies:
- Utils don't import from routers or adapters
- Schemas are standalone
- Config is imported by everyone but imports nothing

## Documentation Standards

### Module Docstrings
Every module should have a docstring:
```python
"""
app/adapters/claude_adapter.py

Adapter for Anthropic Claude API.
Converts between OpenAI-compatible format and Claude's API format.
"""
```

### Class Docstrings
Document the purpose and usage:
```python
class ClaudeAdapter(BaseAdapter):
    """
    Adapter for Anthropic Claude API.

    Converts OpenAI-compatible requests to Claude format and vice versa.
    Handles message format conversion, streaming, and response normalization.
    """
```

### Function Docstrings
Document parameters and return values:
```python
async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a chat completion using Claude API.

    Args:
        request: Normalized request in OpenAI format

    Returns:
        Response in OpenAI-compatible format

    Raises:
        Exception: If Claude API returns an error
    """
```

## Next Steps

- Review the [Testing Guide](./testing.md) to understand testing patterns
- Check [Adding Providers](./adding-providers.md) to see how components work together
- Read [Contributing Guidelines](./contributing.md) for code standards
