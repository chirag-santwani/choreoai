# Models

List and explore all available AI models across different providers.

## Endpoint

```
GET /v1/models
```

## Request Example

```bash
curl http://localhost:8000/v1/models \
  -H "Authorization: Bearer your-api-key"
```

## Response Format

```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4",
      "object": "model",
      "created": 1687882400,
      "owned_by": "openai",
      "permission": [],
      "root": "gpt-4",
      "parent": null
    },
    {
      "id": "claude-3-opus-20240229",
      "object": "model",
      "created": 1709251200,
      "owned_by": "anthropic",
      "permission": [],
      "root": "claude-3-opus-20240229",
      "parent": null
    }
  ]
}
```

## Available Models

### OpenAI Models

| Model ID | Context Length | Description |
|----------|----------------|-------------|
| `gpt-4-turbo-preview` | 128K tokens | Most capable GPT-4 model with extended context |
| `gpt-4` | 8K tokens | Advanced reasoning and complex tasks |
| `gpt-4-32k` | 32K tokens | Extended context window version of GPT-4 |
| `gpt-3.5-turbo` | 16K tokens | Fast and cost-effective for simple tasks |
| `gpt-3.5-turbo-16k` | 16K tokens | Extended context version of GPT-3.5 |

### Claude (Anthropic) Models

| Model ID | Context Length | Description |
|----------|----------------|-------------|
| `claude-3-opus-20240229` | 200K tokens | Most capable Claude model for complex tasks |
| `claude-3-sonnet-20240229` | 200K tokens | Balanced performance and speed |
| `claude-3-haiku-20240307` | 200K tokens | Fastest Claude model for simple tasks |
| `claude-2.1` | 200K tokens | Previous generation, strong performance |
| `claude-2.0` | 100K tokens | Legacy model |

### Azure OpenAI Models

Azure OpenAI models use deployment names configured in your Azure resource:

| Deployment Name | Base Model | Description |
|-----------------|------------|-------------|
| *your-deployment* | GPT-4 | Custom deployment name |
| *your-deployment* | GPT-3.5 | Custom deployment name |

!!! note
    Azure model names are configured by you during deployment creation.

### Google Gemini Models

| Model ID | Context Length | Description |
|----------|----------------|-------------|
| `gemini-pro` | 32K tokens | Gemini's most capable model |
| `gemini-pro-vision` | 16K tokens | Multimodal model supporting images |

### Embedding Models

| Model ID | Dimensions | Provider |
|----------|------------|----------|
| `text-embedding-ada-002` | 1536 | OpenAI |
| `text-embedding-3-small` | 1536 | OpenAI |
| `text-embedding-3-large` | 3072 | OpenAI |

## Get Specific Model

```
GET /v1/models/{model_id}
```

### Request Example

```bash
curl http://localhost:8000/v1/models/gpt-4 \
  -H "Authorization: Bearer your-api-key"
```

### Response Example

```json
{
  "id": "gpt-4",
  "object": "model",
  "created": 1687882400,
  "owned_by": "openai",
  "permission": [],
  "root": "gpt-4",
  "parent": null
}
```

## Model Selection Guide

### By Use Case

**Complex Reasoning & Analysis**
- `gpt-4-turbo-preview`
- `claude-3-opus-20240229`

**Balanced Performance**
- `gpt-4`
- `claude-3-sonnet-20240229`
- `gemini-pro`

**Fast & Cost-Effective**
- `gpt-3.5-turbo`
- `claude-3-haiku-20240307`

**Long Context**
- `claude-3-opus-20240229` (200K tokens)
- `gpt-4-turbo-preview` (128K tokens)
- `gpt-4-32k` (32K tokens)

### By Cost (Approximate, per 1M tokens)

| Model | Input Cost | Output Cost |
|-------|-----------|-------------|
| `gpt-3.5-turbo` | $0.50 | $1.50 |
| `claude-3-haiku-20240307` | $0.25 | $1.25 |
| `gpt-4` | $30.00 | $60.00 |
| `claude-3-sonnet-20240229` | $3.00 | $15.00 |
| `claude-3-opus-20240229` | $15.00 | $75.00 |
| `gpt-4-turbo-preview` | $10.00 | $30.00 |

!!! note
    Prices are approximate and subject to change. Check provider websites for current pricing.

### By Speed

**Fastest**
1. `gpt-3.5-turbo`
2. `claude-3-haiku-20240307`
3. `gemini-pro`

**Medium**
4. `claude-3-sonnet-20240229`
5. `gpt-4`

**Slower (but more capable)**
6. `gpt-4-turbo-preview`
7. `claude-3-opus-20240229`

## Code Examples

### List All Models

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# List all models
models = client.models.list()

for model in models.data:
    print(f"Model: {model.id} (owned by {model.owned_by})")
```

### Get Specific Model

```python
model = client.models.retrieve("gpt-4")
print(f"Model: {model.id}")
print(f"Owner: {model.owned_by}")
```

### Filter by Provider

```python
models = client.models.list()

# Filter OpenAI models
openai_models = [m for m in models.data if m.owned_by == "openai"]

# Filter Claude models
claude_models = [m for m in models.data if m.owned_by == "anthropic"]

print(f"OpenAI models: {[m.id for m in openai_models]}")
print(f"Claude models: {[m.id for m in claude_models]}")
```

### Check Model Availability

```python
def is_model_available(model_id):
    try:
        client.models.retrieve(model_id)
        return True
    except Exception:
        return False

if is_model_available("gpt-4"):
    print("GPT-4 is available")
else:
    print("GPT-4 is not available")
```

## Model Routing

ChoreoAI automatically routes requests to the appropriate provider based on the model name:

```python
# Routes to OpenAI
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)

# Routes to Anthropic
response = client.chat.completions.create(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": "Hello"}]
)

# Routes to Google
response = client.chat.completions.create(
    model="gemini-pro",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Provider Configuration

Models are only available if their provider API keys are configured:

```bash
# .env file
OPENAI_API_KEY=sk-...           # Enables OpenAI models
ANTHROPIC_API_KEY=sk-ant-...    # Enables Claude models
AZURE_OPENAI_API_KEY=...        # Enables Azure models
GEMINI_API_KEY=...              # Enables Gemini models
```

See [Provider Configuration](../providers/README.md) for details.

## Error Responses

### Model Not Found

```json
{
  "error": {
    "message": "Model 'invalid-model' not found",
    "type": "invalid_request_error",
    "code": "model_not_found"
  }
}
```

### Provider Not Configured

```json
{
  "error": {
    "message": "Provider not configured for model 'gpt-4'",
    "type": "invalid_request_error",
    "code": "provider_not_configured"
  }
}
```

## Best Practices

### 1. Choose Based on Requirements

Consider your needs:
- **Quality**: Use GPT-4 or Claude Opus for best results
- **Speed**: Use GPT-3.5 or Claude Haiku for fast responses
- **Cost**: Use smaller models for simple tasks
- **Context**: Use Claude for very long documents

### 2. Test Multiple Models

Different models excel at different tasks:

```python
models_to_test = ["gpt-4", "claude-3-sonnet-20240229", "gemini-pro"]

for model in models_to_test:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Explain quantum computing"}]
    )
    print(f"\n{model}:\n{response.choices[0].message.content}")
```

### 3. Implement Fallbacks

Use fallback models for reliability:

```python
def chat_with_fallback(messages):
    models = ["gpt-4", "claude-3-sonnet-20240229", "gpt-3.5-turbo"]

    for model in models:
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages
            )
        except Exception as e:
            print(f"{model} failed: {e}")
            continue

    raise Exception("All models failed")
```

### 4. Monitor Usage

Track which models you use most:

```python
from collections import Counter

model_usage = Counter()

def track_usage(model):
    model_usage[model] += 1

# Use tracking
track_usage("gpt-4")
print(f"Model usage: {model_usage}")
```

## Next Steps

- **[Chat Completions](chat-completions.md)** - Use models for chat
- **[Providers](../providers/README.md)** - Configure providers
- **[Cost Optimization](../examples/cost-optimization.md)** - Reduce costs
- **[Multi-Provider](../examples/multi-provider.md)** - Use multiple providers
