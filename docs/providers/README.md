# AI Providers Overview

ChoreoAI supports multiple AI providers through a unified API interface. This allows you to switch between providers without changing your application code, enabling flexibility, redundancy, and cost optimization.

## Supported Providers

| Provider | Status | Chat | Streaming | Embeddings | Function Calling |
|----------|--------|------|-----------|------------|------------------|
| [OpenAI](#openai) | ✅ Full Support | ✅ | ✅ | ✅ | ✅ |
| [Claude (Anthropic)](#claude) | ✅ Full Support | ✅ | ✅ | ❌ | ✅ |
| [Azure OpenAI](#azure-openai) | 🚧 In Development | 🚧 | 🚧 | 🚧 | 🚧 |
| [Google Gemini](#google-gemini) | 🚧 In Development | 🚧 | 🚧 | 🚧 | 🚧 |

## How It Works

ChoreoAI acts as a unified gateway that:

1. **Receives requests** in OpenAI-compatible format
2. **Routes to the appropriate provider** based on the model specified
3. **Translates requests** to the provider's native format
4. **Converts responses** back to OpenAI-compatible format
5. **Returns unified responses** to your application

```
Your App → ChoreoAI → Provider (OpenAI/Claude/Azure/Gemini)
         ←          ←
```

## Provider Selection

The provider is automatically selected based on the model name in your request:

```python
# Uses OpenAI
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Uses Claude
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Uses Azure OpenAI
response = client.chat.completions.create(
    model="gpt-35-turbo",  # Azure model name
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Configuration

Each provider requires its own API key and configuration. Set these as environment variables:

```bash
# OpenAI
export OPENAI_API_KEY=sk-...

# Claude (Anthropic)
export ANTHROPIC_API_KEY=sk-ant-...

# Azure OpenAI
export AZURE_OPENAI_API_KEY=...
export AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# Google Gemini
export GEMINI_API_KEY=...
```

## Quick Start by Provider

### OpenAI
```bash
# Set API key
export OPENAI_API_KEY=sk-...

# Make request
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Hello!"}]}'
```

**[Full OpenAI Documentation →](openai.md)**

### Claude (Anthropic)
```bash
# Set API key
export ANTHROPIC_API_KEY=sk-ant-...

# Make request
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
  -d '{"model": "claude-3-5-sonnet-20241022", "messages": [{"role": "user", "content": "Hello!"}]}'
```

**[Full Claude Documentation →](claude.md)**

### Azure OpenAI
```bash
# Set credentials
export AZURE_OPENAI_API_KEY=...
export AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# Make request (coming soon)
```

**[Full Azure OpenAI Documentation →](azure-openai.md)**

### Google Gemini
```bash
# Set API key
export GEMINI_API_KEY=...

# Make request (coming soon)
```

**[Full Gemini Documentation →](gemini.md)**

## Provider Comparison

### Pricing (Approximate)
| Provider | Model | Input (per 1M tokens) | Output (per 1M tokens) |
|----------|-------|---------------------|----------------------|
| OpenAI | GPT-4 Turbo | $10 | $30 |
| OpenAI | GPT-4o | $5 | $15 |
| OpenAI | GPT-3.5 Turbo | $0.50 | $1.50 |
| Claude | Claude 3.5 Sonnet | $3 | $15 |
| Claude | Claude 3 Opus | $15 | $75 |
| Claude | Claude 3 Haiku | $0.25 | $1.25 |
| Azure | Varies by region | Varies | Varies |
| Gemini | Gemini Pro | Free tier available | Free tier available |

### Context Windows
| Provider | Model | Context Window |
|----------|-------|----------------|
| OpenAI | GPT-4 Turbo | 128K tokens |
| OpenAI | GPT-4o | 128K tokens |
| OpenAI | GPT-3.5 Turbo | 16K tokens |
| Claude | Claude 3.5 Sonnet | 200K tokens |
| Claude | Claude 3 Opus | 200K tokens |
| Claude | Claude 3 Haiku | 200K tokens |
| Gemini | Gemini 1.5 Pro | 2M tokens |

### Rate Limits
Rate limits vary by provider tier and subscription. See individual provider documentation for details.

## Best Practices

### 1. Environment Variables
Store API keys securely using environment variables, never in code:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="http://localhost:8000/v1"
)
```

### 2. Provider Failover
Implement fallback logic to switch providers if one fails:

```python
def chat_with_fallback(messages):
    providers = [
        {"model": "gpt-4", "provider": "OpenAI"},
        {"model": "claude-3-5-sonnet-20241022", "provider": "Claude"},
    ]

    for config in providers:
        try:
            response = client.chat.completions.create(
                model=config["model"],
                messages=messages
            )
            return response
        except Exception as e:
            print(f"{config['provider']} failed: {e}")
            continue

    raise Exception("All providers failed")
```

### 3. Cost Optimization
Choose the right model for your use case:

- **Simple tasks**: Use GPT-3.5 Turbo or Claude Haiku
- **Complex reasoning**: Use GPT-4 or Claude Opus
- **Balanced performance**: Use GPT-4o or Claude Sonnet
- **High volume**: Consider Gemini's free tier

### 4. Model Selection Strategy
```python
def select_model(task_complexity, budget):
    if budget == "low":
        return "gpt-3.5-turbo" if task_complexity == "simple" else "claude-3-haiku-20240307"
    elif budget == "medium":
        return "gpt-4o" if task_complexity == "complex" else "claude-3-5-sonnet-20241022"
    else:
        return "gpt-4" if task_complexity == "very_complex" else "claude-3-opus-20240229"
```

## Common Features Across Providers

### Streaming
All providers support streaming responses:

```python
response = client.chat.completions.create(
    model="gpt-4",  # or any other model
    messages=[{"role": "user", "content": "Write a story"}],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### System Messages
Most providers support system messages for context:

```python
messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "Explain async/await in Python"}
]
```

### Temperature Control
Adjust creativity with the temperature parameter (0.0 to 2.0):

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    temperature=0.7  # 0 = deterministic, 2 = very creative
)
```

## Provider-Specific Features

### OpenAI Only
- **Function Calling**: Advanced function/tool calling
- **Vision**: GPT-4V for image understanding
- **DALL-E**: Image generation
- **Whisper**: Speech-to-text
- **TTS**: Text-to-speech

### Claude Only
- **Extended Context**: Up to 200K tokens
- **Constitutional AI**: Built-in safety features
- **JSON Mode**: Structured output support

### Azure OpenAI Only
- **Enterprise Features**: Private endpoints, VNet integration
- **Compliance**: Additional certifications
- **SLA**: Enterprise-grade SLA

### Gemini Only
- **Massive Context**: Up to 2M tokens
- **Multimodal**: Native image, video, and audio support
- **Free Tier**: Generous free usage limits

## Troubleshooting

### Authentication Errors
```
Error: Invalid API key
```

**Solution**: Verify your API key is set correctly:
```bash
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
```

### Model Not Found
```
Error: Model 'gpt-5' not found
```

**Solution**: Check available models:
```bash
curl http://localhost:8000/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Rate Limit Errors
```
Error: Rate limit exceeded
```

**Solution**:
1. Implement exponential backoff
2. Reduce request frequency
3. Upgrade your provider tier
4. Switch to a different provider

### Provider Connection Issues
```
Error: Failed to connect to provider
```

**Solution**:
1. Check internet connectivity
2. Verify provider status page
3. Check API key permissions
4. Review firewall/proxy settings

## Next Steps

1. **Choose Your Provider**: Review individual provider documentation
2. **Get API Keys**: Sign up and obtain credentials
3. **Configure ChoreoAI**: Set environment variables
4. **Test Connection**: Make your first request
5. **Implement Fallback**: Set up multi-provider redundancy

## Provider Documentation

- **[OpenAI Provider Guide](openai.md)** - Complete OpenAI setup and usage
- **[Claude Provider Guide](claude.md)** - Anthropic Claude configuration
- **[Azure OpenAI Guide](azure-openai.md)** - Azure OpenAI deployment
- **[Google Gemini Guide](gemini.md)** - Google Gemini integration

## Support

For provider-specific issues:
- **OpenAI**: [OpenAI Help Center](https://help.openai.com)
- **Claude**: [Anthropic Support](https://support.anthropic.com)
- **Azure**: [Azure Support](https://azure.microsoft.com/support)
- **Gemini**: [Google AI Support](https://ai.google.dev/support)

For ChoreoAI integration issues:
- GitHub Issues: [github.com/choreoai/issues](https://github.com/choreoai/issues)
- Documentation: [Full docs](../README.md)
