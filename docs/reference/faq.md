# Frequently Asked Questions (FAQ)

Common questions and answers about ChoreoAI.

## General Questions

### What is ChoreoAI?

ChoreoAI is a unified API orchestration platform that provides a single, standardized interface to interact with multiple AI providers. Instead of learning different APIs for OpenAI, Claude, Gemini, and other providers, you can use one consistent API for all your AI needs.

### Why use ChoreoAI instead of calling providers directly?

**Benefits of using ChoreoAI:**
- **Single API**: One interface for all providers
- **Easy switching**: Change models without code changes
- **OpenAI-compatible**: Works with existing OpenAI code
- **Fallback support**: Automatic failover between providers
- **Cost optimization**: Route to cheaper models automatically
- **Simplified deployment**: One service to manage
- **Unified error handling**: Consistent error responses

### Is ChoreoAI open source?

Yes, ChoreoAI is open source. You can view the code, contribute, and use it freely for your projects.

### What AI providers does ChoreoAI support?

ChoreoAI currently supports:
- **OpenAI** (GPT-4, GPT-3.5)
- **Anthropic** (Claude 3 Opus, Sonnet, Haiku)
- **Azure OpenAI** (GPT-4, GPT-3.5 via Azure)
- **Google Gemini** (Gemini Pro, Pro Vision)
- **xAI** (Grok models)
- **AWS Bedrock** (Various foundation models)

### Can I add support for additional providers?

Yes! ChoreoAI is designed to be extensible. You can add new providers by creating an adapter that implements the base adapter interface. See the [Adding Providers](../development/adding-providers.md) guide.

## Getting Started

### How do I get started with ChoreoAI?

1. **Install the Python client**:
   ```bash
   pip install choreoai
   ```

2. **Set your API key**:
   ```bash
   export CHOREOAI_API_KEY=your-api-key
   ```

3. **Make your first request**:
   ```python
   from choreoai import ChoreoAI

   client = ChoreoAI()
   response = client.chat.completions.create(
       model="gpt-4",
       messages=[{"role": "user", "content": "Hello!"}]
   )
   print(response.choices[0].message.content)
   ```

See the [Quick Start Guide](../client/quickstart.md) for details.

### Do I need API keys for all providers?

No, you only need API keys for the providers you want to use. Configure at least one provider to get started. The API will only route requests to providers that are properly configured.

### How do I get provider API keys?

- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Anthropic (Claude)**: [console.anthropic.com](https://console.anthropic.com)
- **Google Gemini**: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- **Azure OpenAI**: [portal.azure.com](https://portal.azure.com) (requires Azure subscription)

### Is ChoreoAI compatible with OpenAI's SDK?

Yes! ChoreoAI is OpenAI-compatible. You can use the OpenAI Python SDK by changing the `base_url`:

```python
import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = "your-choreoai-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Authentication & Security

### How does authentication work?

ChoreoAI uses API key-based authentication. Include your API key in the `Authorization` header:

```bash
Authorization: Bearer your-api-key
```

See [Authentication Guide](../api/authentication.md) for details.

### Where do I get a ChoreoAI API key?

For local development, you can use any string as your API key. The default configuration accepts all keys.

For production, implement proper API key validation in your deployment. Consider using a database or secret management service to manage keys.

### Are my API keys secure?

Provider API keys (OpenAI, Claude, etc.) are stored server-side as environment variables and are never exposed to clients. Clients only need the ChoreoAI API key to make requests.

**Security best practices:**
- Never commit API keys to version control
- Use environment variables or secret managers
- Rotate keys regularly
- Use different keys for different environments
- Implement rate limiting and monitoring

### Can I use ChoreoAI without authentication?

Authentication middleware can be disabled for development, but this is **not recommended for production**. Always use authentication in production environments.

## Usage & Features

### Can I use streaming responses?

Yes! ChoreoAI supports streaming for real-time responses:

```python
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a poem"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

See [Streaming Guide](../client/streaming.md) for details.

### Does ChoreoAI support async/await?

Yes! Use the `AsyncChoreoAI` client:

```python
from choreoai import AsyncChoreoAI
import asyncio

async def main():
    client = AsyncChoreoAI()
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

See [Async Usage Guide](../client/async-usage.md) for details.

### Can I create embeddings with ChoreoAI?

Yes! Use the embeddings endpoint:

```python
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Text to embed"
)

embedding = response.data[0].embedding
```

See [Embeddings Guide](../api/embeddings.md) for details.

### How do I switch between providers?

Simply change the model name in your request:

```python
# Use OpenAI
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)

# Use Claude
response = client.chat.completions.create(
    model="claude-3-sonnet-20240229",
    messages=[{"role": "user", "content": "Hello"}]
)

# Use Gemini
response = client.chat.completions.create(
    model="gemini-pro",
    messages=[{"role": "user", "content": "Hello"}]
)
```

ChoreoAI automatically routes to the correct provider based on the model name.

### Can I implement fallback between providers?

Yes! Here's a simple fallback implementation:

```python
def chat_with_fallback(messages):
    models = ["gpt-4", "claude-3-sonnet-20240229", "gemini-pro"]

    for model in models:
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages
            )
        except Exception as e:
            print(f"{model} failed: {e}")
            continue

    raise Exception("All providers failed")
```

## Deployment & Operations

### How do I deploy ChoreoAI?

ChoreoAI supports multiple deployment options:

**Docker:**
```bash
docker build -t choreoai .
docker run -p 8000:8000 choreoai
```

**Docker Compose:**
```bash
docker-compose up
```

**Kubernetes:**
```bash
kubectl apply -f k8s/
```

**Helm:**
```bash
helm install choreoai ./helm/choreoai
```

See [Deployment Guide](../deployment/README.md) for details.

### What are the system requirements?

**Minimum:**
- Python 3.9+
- 512MB RAM
- 1 CPU core

**Recommended:**
- Python 3.11+
- 2GB RAM
- 2+ CPU cores
- SSD storage

**For production:**
- 4GB+ RAM
- 4+ CPU cores
- Load balancer
- Monitoring solution

### How do I scale ChoreoAI?

ChoreoAI is stateless and can be easily scaled horizontally:

**Kubernetes HPA:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: choreoai-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: choreoai
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Docker Swarm:**
```bash
docker service scale choreoai=5
```

### How do I monitor ChoreoAI?

ChoreoAI provides several monitoring options:

1. **Logs**: Structured logging with configurable levels
2. **Health checks**: `/health` endpoint for uptime monitoring
3. **Metrics**: Integration with Prometheus (optional)
4. **Distributed tracing**: OpenTelemetry support (optional)

See [Monitoring Guide](../deployment/monitoring.md) for details.

### Can I run ChoreoAI on serverless platforms?

ChoreoAI uses FastAPI which supports serverless deployment, but:
- Cold starts may impact latency
- Streaming requires connection persistence
- Consider serverless containers (AWS Fargate, Google Cloud Run)

## Troubleshooting

### Why am I getting "Model not found" errors?

**Possible causes:**
1. Model name is misspelled
2. Provider API key is not configured
3. Provider is not enabled

**Solutions:**
- Verify model name spelling
- Check provider API key is set in environment variables
- List available models: `client.models.list()`
- Verify provider configuration

### Why are my requests timing out?

**Possible causes:**
1. Provider API is slow or down
2. Request timeout is too short
3. Network connectivity issues
4. Large context/response size

**Solutions:**
- Increase timeout: `client = ChoreoAI(timeout=60.0)`
- Check provider status pages
- Implement retry logic
- Use streaming for long responses
- Reduce context length

### How do I handle rate limits?

Implement exponential backoff retry:

```python
import time

def exponential_backoff_retry(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if hasattr(e, 'status_code') and e.status_code == 429:
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Why am I getting authentication errors?

**Common issues:**
1. Missing Authorization header
2. Incorrect API key format
3. API key not set in environment

**Solutions:**
- Ensure header format: `Authorization: Bearer your-key`
- Check for typos in API key
- Verify environment variables are loaded
- Test with: `curl -H "Authorization: Bearer test" http://localhost:8000/v1/models`

### How do I debug API requests?

**Enable debug logging:**
```bash
LOG_LEVEL=DEBUG python -m uvicorn app.main:app
```

**Log request/response:**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    response = client.chat.completions.create(...)
    logger.debug(f"Response: {response}")
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
```

**Use verbose mode (if available):**
```python
client = ChoreoAI(api_key="your-key", verbose=True)
```

## Costs & Pricing

### Does ChoreoAI charge for usage?

ChoreoAI itself is free and open source. However, you pay for the underlying provider usage (OpenAI, Claude, etc.) based on their pricing.

### How can I reduce costs?

**Strategies:**
1. **Use cheaper models**: GPT-3.5 instead of GPT-4 for simple tasks
2. **Optimize prompts**: Reduce token usage with concise prompts
3. **Cache responses**: Store and reuse responses for common queries
4. **Set max_tokens**: Limit response length to control costs
5. **Batch requests**: Combine multiple queries when possible
6. **Use fallbacks**: Route to cheaper providers automatically

**Example cost comparison (per 1M tokens):**
- GPT-3.5-turbo: ~$0.50 input, $1.50 output
- Claude Haiku: ~$0.25 input, $1.25 output
- GPT-4: ~$30 input, $60 output
- Claude Opus: ~$15 input, $75 output

### How do I track usage and costs?

1. **Token counting**: Track tokens from response.usage
2. **Request logging**: Log all requests with model and tokens
3. **Provider dashboards**: Check OpenAI, Claude dashboards
4. **Custom analytics**: Build usage tracking in your application

```python
# Track usage
total_tokens = 0

response = client.chat.completions.create(...)
total_tokens += response.usage.total_tokens

print(f"Total tokens used: {total_tokens}")
```

## Development

### How do I contribute to ChoreoAI?

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

See [Contributing Guide](../development/contributing.md) for details.

### How do I run tests?

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=choreoai

# Run specific test file
pytest tests/test_client.py
```

### How do I add a new provider?

Create an adapter class that implements the base adapter interface:

```python
from app.adapters.base import BaseAdapter

class NewProviderAdapter(BaseAdapter):
    def chat_completion(self, request):
        # Implement provider-specific logic
        pass

    def stream_chat_completion(self, request):
        # Implement streaming
        pass
```

See [Adding Providers Guide](../development/adding-providers.md) for details.

### Where can I find code examples?

Examples are available in multiple places:
- **[Examples Directory](../../examples/)** - Working code examples
- **[Documentation Examples](../examples/README.md)** - Tutorials and guides
- **[API Docs](../api/README.md)** - Request/response examples
- **[GitHub Repository](https://github.com/choreoai)** - Source code

## Advanced Topics

### Can I use custom models?

Yes, if your provider supports custom fine-tuned models, you can use them by specifying the model ID:

```python
response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo:custom-model-id",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Does ChoreoAI support function calling?

Function calling support depends on the underlying provider. OpenAI and some other providers support it:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Boston?"}],
    functions=[{
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    }]
)
```

### Can I use ChoreoAI with LangChain?

Yes! ChoreoAI's OpenAI compatibility makes it work with LangChain:

```python
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    openai_api_base="http://localhost:8000/v1",
    openai_api_key="your-choreoai-api-key",
    model_name="gpt-4"
)
```

### How do I implement request validation?

ChoreoAI uses Pydantic for automatic validation. Custom validation can be added:

```python
from pydantic import validator

class CustomChatRequest(ChatRequest):
    @validator('temperature')
    def validate_temperature(cls, v):
        if not 0 <= v <= 2:
            raise ValueError('Temperature must be between 0 and 2')
        return v
```

### Can I customize error responses?

Yes, you can customize error handling with middleware:

```python
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class CustomErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            # Custom error handling
            return Response(
                content=custom_error_response(e),
                status_code=500
            )
```

## Support & Community

### Where can I get help?

- **Documentation**: [docs](../README.md)
- **GitHub Issues**: [Report bugs or request features](https://github.com/choreoai/choreoai/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/choreoai/choreoai/discussions)
- **Examples**: [Working code examples](../../examples/)

### How do I report a bug?

1. Check if the issue already exists
2. Create a new issue on GitHub
3. Include:
   - ChoreoAI version
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### How do I request a feature?

1. Check if the feature is already requested
2. Create a feature request on GitHub
3. Describe:
   - Use case and motivation
   - Proposed solution
   - Alternative solutions considered
   - Additional context

### Is there a roadmap?

Yes! Check the project roadmap on GitHub for planned features and improvements.

## Related Documentation

- **[Quick Start](../client/quickstart.md)** - Get started guide
- **[API Reference](../api/README.md)** - Complete API documentation
- **[Deployment Guide](../deployment/README.md)** - Deployment options
- **[Error Codes](error-codes.md)** - Error reference
- **[Environment Variables](environment-vars.md)** - Configuration reference
- **[Glossary](glossary.md)** - Terms and definitions
