# API Documentation

## Introduction

ChoreoAI provides a RESTful API that follows the OpenAI API specification, making it a drop-in replacement for OpenAI's API while supporting multiple providers including Claude, Azure OpenAI, and Google Gemini.

## Base URL

```
http://localhost:8000
```

For production deployments, replace with your actual domain:
```
https://api.yourcompany.com
```

## Authentication

All API requests require authentication using an API key passed in the Authorization header:

```bash
Authorization: Bearer your-api-key
```

See [Authentication](authentication.md) for detailed information.

## Available Endpoints

### Chat Completions
```
POST /v1/chat/completions
```
Create chat completions using any supported AI model. Supports streaming and function calling.

**[View Documentation →](chat-completions.md)**

### Embeddings
```
POST /v1/embeddings
```
Generate vector embeddings for text inputs.

**[View Documentation →](embeddings.md)**

### Models
```
GET /v1/models
```
List all available models across providers.

**[View Documentation →](models.md)**

### Health Check
```
GET /health
```
Check API health status.

## Quick Example

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of France?"}
    ],
    "temperature": 0.7,
    "max_tokens": 150
  }'
```

Response:
```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1699564800,
  "model": "gpt-4",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The capital of France is Paris."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 8,
    "total_tokens": 28
  }
}
```

## Content Type

All requests must include the `Content-Type: application/json` header.

## Rate Limiting

Rate limits depend on your configured provider:
- OpenAI: Based on your OpenAI tier
- Claude: Based on your Anthropic tier
- Azure OpenAI: Based on your Azure deployment
- Gemini: Based on your Google AI quota

See individual [provider documentation](../providers/README.md) for specific limits.

## Error Handling

The API returns standard HTTP status codes and structured error responses:

```json
{
  "error": {
    "message": "Invalid API key provided",
    "type": "authentication_error",
    "code": "invalid_api_key"
  }
}
```

See [Error Handling](error-handling.md) for complete documentation.

## OpenAI Compatibility

ChoreoAI is designed to be compatible with OpenAI's API. You can use it as a drop-in replacement by changing the base URL:

```python
# OpenAI SDK with ChoreoAI
import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Next Steps

- **[Authentication](authentication.md)** - Learn how to authenticate requests
- **[Chat Completions](chat-completions.md)** - Generate chat responses
- **[Streaming](streaming.md)** - Use Server-Sent Events for real-time responses
- **[Error Handling](error-handling.md)** - Handle errors gracefully
