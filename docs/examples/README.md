# ChoreoAI Examples Documentation

Complete examples and tutorials for using ChoreoAI to orchestrate multiple AI providers.

## Overview

ChoreoAI is a unified API orchestration platform that provides a single OpenAI-compatible interface for multiple AI providers. These examples demonstrate how to leverage ChoreoAI's features including multi-provider support, fallback strategies, cost optimization, and more.

## Quick Navigation

### Getting Started
- [Basic Usage](basic-usage.md) - Learn the fundamentals of using ChoreoAI
- [Installation Guide](../client/installation.md) - Install the ChoreoAI client

### Advanced Features
- [Multi-Provider Usage](multi-provider.md) - Use multiple AI providers seamlessly
- [Fallback Strategy](fallback-strategy.md) - Implement robust failover mechanisms
- [Cost Optimization](cost-optimization.md) - Optimize AI costs across providers

### Additional Resources
- [API Reference](../api/README.md) - Complete API documentation
- [Deployment Guide](../deployment/README.md) - Deploy ChoreoAI in production

## What You'll Learn

### Basic Usage Tutorial
Start here if you're new to ChoreoAI. Learn how to:
- Set up the ChoreoAI client
- Make your first API call
- Handle responses and errors
- Work with streaming responses
- Build multi-turn conversations

**Time to complete:** 10 minutes

### Multi-Provider Guide
Learn how to work with multiple AI providers:
- Switch between OpenAI, Claude, Gemini, and more
- Compare responses from different models
- Choose the right model for your use case
- Handle provider-specific features

**Time to complete:** 15 minutes

### Fallback Strategy Guide
Build resilient applications with automatic failover:
- Configure fallback chains
- Handle provider outages gracefully
- Implement retry logic
- Monitor fallback events

**Time to complete:** 20 minutes

### Cost Optimization Guide
Reduce AI costs without sacrificing quality:
- Route requests to cost-effective models
- Implement intelligent model selection
- Track and analyze spending
- Optimize token usage

**Time to complete:** 25 minutes

## Prerequisites

Before starting these examples, make sure you have:

1. **Python 3.9 or higher** installed
2. **ChoreoAI API** running (locally or remote)
3. **At least one provider API key** (OpenAI, Anthropic, Google, etc.)
4. **ChoreoAI Python client** installed

### Quick Setup

```bash
# Install ChoreoAI client
pip install choreoai

# Set up environment variables
export CHOREOAI_API_KEY=your-api-key
export OPENAI_API_KEY=your-openai-key

# Verify installation
python -c "from choreoai import ChoreoAI; print('ChoreoAI installed successfully!')"
```

## Example Code Repository

All example code is available in the `/examples` directory:

```
examples/
├── basic_usage.py          # Basic chat completion
├── streaming.py            # Streaming responses
├── embeddings_rag.py       # Embeddings and RAG
├── function_calling.py     # Function/tool calling
├── list_models.py          # List available models
├── fallback.py            # Fallback strategies
├── cost_optimization.py   # Cost optimization
└── ab_testing.py          # A/B testing
```

## Running Examples

### Option 1: Using the Client Library

Most examples in this documentation use the ChoreoAI Python client:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

### Option 2: Using OpenAI SDK

You can also use the OpenAI SDK with ChoreoAI's base URL:

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

Both approaches work identically with ChoreoAI!

## Key Concepts

### Unified API
ChoreoAI provides a single OpenAI-compatible API that works with multiple providers:
- **OpenAI** (GPT-3.5, GPT-4, GPT-4 Turbo)
- **Anthropic** (Claude 3 Haiku, Sonnet, Opus)
- **Google** (Gemini Pro, Gemini Ultra)
- **xAI** (Grok)
- **Azure OpenAI**
- **AWS Bedrock**

### Provider Routing
Requests are automatically routed to the appropriate provider based on the model name:
- `gpt-4` → OpenAI
- `claude-3-sonnet-20240229` → Anthropic
- `gemini-pro` → Google

### Compatibility
Full compatibility with OpenAI SDK means:
- Drop-in replacement for existing code
- No need to learn new APIs
- Switch providers by changing model name only

## Common Use Cases

### 1. Chat Applications
Build conversational AI applications with:
- Multi-turn conversations
- Context management
- Streaming responses
- Function calling

**See:** [Basic Usage](basic-usage.md)

### 2. Multi-Model Systems
Use multiple AI models in the same application:
- Compare model responses
- Choose best model for task
- A/B test different providers

**See:** [Multi-Provider Guide](multi-provider.md)

### 3. High Availability
Build resilient systems with:
- Automatic failover
- Provider redundancy
- Graceful degradation

**See:** [Fallback Strategy](fallback-strategy.md)

### 4. Cost Management
Optimize AI spending with:
- Intelligent model routing
- Cost tracking
- Budget controls

**See:** [Cost Optimization](cost-optimization.md)

## Architecture Overview

```
Your Application
       ↓
ChoreoAI Client
       ↓
ChoreoAI API Gateway
       ↓
    ┌──┴──┬──────┬──────┐
    ↓     ↓      ↓      ↓
 OpenAI Claude Gemini Grok
```

### How It Works

1. **Request**: Your app sends a request to ChoreoAI
2. **Routing**: ChoreoAI determines the provider based on model name
3. **Translation**: Request is translated to provider-specific format
4. **Execution**: Provider processes the request
5. **Response**: ChoreoAI returns standardized response

### Benefits

- **Single Interface**: One API for all providers
- **Easy Switching**: Change models without code changes
- **Resilience**: Automatic failover and retry
- **Cost Control**: Optimize across providers
- **Monitoring**: Centralized logging and metrics

## Best Practices

### 1. Environment Variables
Always use environment variables for API keys:

```python
import os
from choreoai import ChoreoAI

client = ChoreoAI(
    api_key=os.getenv("CHOREOAI_API_KEY")
)
```

### 2. Error Handling
Implement proper error handling:

```python
try:
    response = client.chat.completions.create(...)
except ValueError as e:
    print(f"Invalid parameters: {e}")
except ConnectionError as e:
    print(f"Connection error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 3. Timeout Configuration
Set appropriate timeouts for long-running requests:

```python
client = ChoreoAI(
    api_key="your-api-key",
    timeout=60.0  # 60 seconds
)
```

### 4. Retry Logic
Enable retries for transient failures:

```python
client = ChoreoAI(
    api_key="your-api-key",
    max_retries=3
)
```

### 5. Cost Monitoring
Track token usage and costs:

```python
response = client.chat.completions.create(...)

# Check token usage
print(f"Tokens used: {response.usage.total_tokens}")
print(f"Cost estimate: ${response.usage.total_tokens * 0.002 / 1000}")
```

## Troubleshooting

### Connection Issues

**Problem:** Cannot connect to ChoreoAI
```
ConnectionError: Connection refused
```

**Solution:**
```bash
# Verify ChoreoAI is running
curl http://localhost:8000/health

# Check base URL is correct
export CHOREOAI_BASE_URL=http://localhost:8000
```

### Authentication Errors

**Problem:** Authentication failed
```
AuthenticationError: Invalid API key
```

**Solution:**
```bash
# Verify API key is set
echo $CHOREOAI_API_KEY

# Check API key is valid
curl -H "Authorization: Bearer $CHOREOAI_API_KEY" \
     http://localhost:8000/v1/models
```

### Model Not Found

**Problem:** Requested model is not available
```
Error: Model 'gpt-4' not found
```

**Solution:**
```python
# List available models
models = client.models.list()
for model in models.data:
    print(model.id)

# Check provider API key is configured on server
```

### Rate Limiting

**Problem:** Too many requests
```
RateLimitError: Rate limit exceeded
```

**Solution:**
```python
import time

# Implement exponential backoff
for attempt in range(3):
    try:
        response = client.chat.completions.create(...)
        break
    except RateLimitError:
        wait_time = 2 ** attempt
        time.sleep(wait_time)
```

## Performance Tips

### 1. Use Streaming for Long Responses
```python
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='')
```

### 2. Optimize Token Usage
```python
# Use max_tokens to limit response length
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[...],
    max_tokens=150  # Limit response
)
```

### 3. Choose Appropriate Models
```python
# Use cheaper models for simple tasks
response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Cheaper than GPT-4
    messages=[...]
)

# Use powerful models only when needed
response = client.chat.completions.create(
    model="gpt-4",  # More expensive but more capable
    messages=[...]
)
```

### 4. Batch Requests When Possible
```python
# Batch embeddings
texts = ["text1", "text2", "text3"]
embeddings = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts  # Process all at once
)
```

## Next Steps

1. **Start with basics**: Complete the [Basic Usage](basic-usage.md) tutorial
2. **Explore providers**: Try the [Multi-Provider Guide](multi-provider.md)
3. **Build resilience**: Implement [Fallback Strategies](fallback-strategy.md)
4. **Optimize costs**: Follow the [Cost Optimization Guide](cost-optimization.md)
5. **Deploy to production**: Review the [Deployment Guide](../deployment/README.md)

## Additional Resources

### Documentation
- [API Documentation](../api/README.md)
- [Client Documentation](../client/README.md)
- [Deployment Guide](../deployment/README.md)

### Example Code
- [GitHub Repository](https://github.com/yourusername/choreoai)
- [Example Scripts](/examples)

### Community
- [GitHub Discussions](https://github.com/yourusername/choreoai/discussions)
- [Issue Tracker](https://github.com/yourusername/choreoai/issues)

## Support

Need help? Here's how to get support:

1. **Check Documentation**: Review the relevant guide
2. **Search Issues**: Look for similar problems on GitHub
3. **Ask Questions**: Post in GitHub Discussions
4. **Report Bugs**: Open an issue with details

## Contributing

We welcome contributions! See the [Contributing Guide](../../CONTRIBUTING.md) for details.

## License

ChoreoAI is released under the MIT License. See [LICENSE](../../LICENSE) for details.
