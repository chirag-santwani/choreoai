# Chat Completions

Generate chat completions using any supported AI model through a unified interface.

## Endpoint

```
POST /v1/chat/completions
```

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Model identifier (e.g., "gpt-4", "claude-3-opus-20240229", "gemini-pro") |
| `messages` | array | Yes | Array of message objects with `role` and `content` |
| `temperature` | number | No | Sampling temperature between 0 and 2. Default: 1.0 |
| `max_tokens` | integer | No | Maximum tokens to generate. Default: provider-specific |
| `stream` | boolean | No | Enable streaming responses. Default: false |
| `top_p` | number | No | Nucleus sampling probability. Default: 1.0 |
| `n` | integer | No | Number of completions to generate. Default: 1 |
| `stop` | string/array | No | Stop sequences to end generation |
| `presence_penalty` | number | No | Penalty for token presence (-2.0 to 2.0). Default: 0 |
| `frequency_penalty` | number | No | Penalty for token frequency (-2.0 to 2.0). Default: 0 |
| `tools` | array | No | Function calling tools definition |
| `tool_choice` | string/object | No | Controls which tool is called |

### Messages Format

Each message must include:
- `role`: One of "system", "user", or "assistant"
- `content`: The message content (string)

```json
[
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "What is the capital of France?"},
  {"role": "assistant", "content": "The capital of France is Paris."},
  {"role": "user", "content": "What is its population?"}
]
```

## Request Example

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant that provides concise answers."
      },
      {
        "role": "user",
        "content": "Explain quantum computing in one sentence."
      }
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

## Response Format

### Standard Response

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
        "content": "Quantum computing uses quantum-mechanical phenomena like superposition and entanglement to perform calculations exponentially faster than classical computers for certain types of problems."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 35,
    "completion_tokens": 28,
    "total_tokens": 63
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the completion |
| `object` | string | Always "chat.completion" |
| `created` | integer | Unix timestamp of creation |
| `model` | string | Model used for completion |
| `choices` | array | Array of completion choices |
| `choices[].index` | integer | Choice index |
| `choices[].message` | object | Generated message |
| `choices[].message.role` | string | Always "assistant" |
| `choices[].message.content` | string | Generated content |
| `choices[].finish_reason` | string | Reason for completion: "stop", "length", "tool_calls" |
| `usage` | object | Token usage information |
| `usage.prompt_tokens` | integer | Tokens in the prompt |
| `usage.completion_tokens` | integer | Tokens in the completion |
| `usage.total_tokens` | integer | Total tokens used |

## Streaming Responses

Enable real-time streaming by setting `stream: true`:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Write a haiku about coding."}],
    "stream": true
  }'
```

### Streaming Response Format

Server-Sent Events (SSE) format:

```
data: {"id":"chatcmpl-abc","object":"chat.completion.chunk","created":1699564800,"model":"gpt-4","choices":[{"index":0,"delta":{"role":"assistant","content":""},"finish_reason":null}]}

data: {"id":"chatcmpl-abc","object":"chat.completion.chunk","created":1699564800,"model":"gpt-4","choices":[{"index":0,"delta":{"content":"Code"},"finish_reason":null}]}

data: {"id":"chatcmpl-abc","object":"chat.completion.chunk","created":1699564800,"model":"gpt-4","choices":[{"index":0,"delta":{"content":" flows"},"finish_reason":null}]}

data: [DONE]
```

See [Streaming Guide](streaming.md) for detailed documentation.

## Function Calling

Define tools that the model can call:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "What'\''s the weather in Boston?"}
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "get_weather",
          "description": "Get the current weather for a location",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "City name"
              }
            },
            "required": ["location"]
          }
        }
      }
    ]
  }'
```

Response with function call:
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
        "content": null,
        "tool_calls": [
          {
            "id": "call_abc123",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\": \"Boston\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

## Model Selection

Use the model parameter to choose any supported model:

### OpenAI Models
- `gpt-4-turbo-preview`
- `gpt-4`
- `gpt-3.5-turbo`

### Claude Models
- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307`

### Gemini Models
- `gemini-pro`
- `gemini-pro-vision`

### Azure OpenAI
- Use your deployment name (e.g., `my-gpt4-deployment`)

See [Models Documentation](models.md) for the complete list.

## Error Responses

### Invalid Model

```json
{
  "error": {
    "message": "Model 'invalid-model' not found",
    "type": "invalid_request_error",
    "code": "model_not_found"
  }
}
```

### Missing Required Parameters

```json
{
  "error": {
    "message": "Missing required parameter: messages",
    "type": "invalid_request_error",
    "code": "missing_parameter"
  }
}
```

### Rate Limit Exceeded

```json
{
  "error": {
    "message": "Rate limit exceeded",
    "type": "rate_limit_error",
    "code": "rate_limit_exceeded"
  }
}
```

See [Error Handling](error-handling.md) for complete error documentation.

## Code Examples

### Python (ChoreoAI Client)

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain AI in simple terms."}
    ],
    temperature=0.7,
    max_tokens=150
)

print(response.choices[0].message.content)
```

### Python (OpenAI Client)

```python
import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### JavaScript/TypeScript

```javascript
const response = await fetch('http://localhost:8000/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-api-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'gpt-4',
    messages: [
      {role: 'system', content: 'You are a helpful assistant.'},
      {role: 'user', content: 'Hello!'}
    ]
  })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

## Best Practices

### 1. Set Appropriate Temperature

- **0.0-0.3**: Factual, deterministic responses
- **0.4-0.7**: Balanced creativity and consistency
- **0.8-1.0**: Creative, varied responses
- **1.0-2.0**: Highly random and creative

### 2. Use System Messages

Guide the model's behavior with system messages:

```json
{
  "messages": [
    {"role": "system", "content": "You are a concise technical writer."},
    {"role": "user", "content": "Explain APIs."}
  ]
}
```

### 3. Limit max_tokens

Control costs and response length:

```json
{
  "max_tokens": 100
}
```

### 4. Handle Errors Gracefully

Always check response status and handle errors:

```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    print(f"Error: {e}")
```

### 5. Use Streaming for Long Responses

Enable streaming for better UX:

```python
for chunk in client.chat.completions.create(..., stream=True):
    print(chunk.choices[0].delta.content, end='')
```

## Next Steps

- **[Streaming](streaming.md)** - Learn about real-time streaming
- **[Models](models.md)** - Explore available models
- **[Error Handling](error-handling.md)** - Handle errors effectively
- **[Client Documentation](../client/chat.md)** - Use the Python SDK
