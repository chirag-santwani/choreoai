# ChoreoAI Documentation

Welcome to **ChoreoAI** - your unified API orchestration platform for multiple AI providers.

## What is ChoreoAI?

ChoreoAI provides a single, standardized API interface to interact with multiple AI providers including OpenAI, Claude, Azure OpenAI, and Google Gemini. Instead of learning different APIs for each provider, use one consistent interface for all your AI needs.

## Key Features

- **🔄 Unified Interface** - One API for OpenAI, Claude, Azure OpenAI, and Gemini
- **🚀 Easy Provider Switching** - Change providers without changing code
- **⚡ OpenAI-Compatible** - Drop-in replacement for OpenAI API
- **🔐 Secure** - API key-based authentication
- **📊 Streaming Support** - Real-time responses with Server-Sent Events
- **🐍 Python SDK** - Official client library with sync and async support
- **🛠️ Production-Ready** - Docker, Kubernetes, and Helm deployment options
- **📈 Extensible** - Easy to add new providers

## Quick Start

### Using the API

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Using the Python Client

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

## Documentation Sections

### 📚 API Reference
Learn about the REST API endpoints, authentication, and request/response formats.
- [API Overview](api/README.md)
- [Authentication](api/authentication.md)
- [Chat Completions](api/chat-completions.md)
- [Embeddings](api/embeddings.md)
- [Models](api/models.md)
- [Streaming](api/streaming.md)
- [Error Handling](api/error-handling.md)

### 🐍 Python Client
Get started with the official Python SDK.
- [Client Overview](client/README.md)
- [Installation](client/installation.md)
- [Quick Start](client/quickstart.md)
- [Chat Completions](client/chat.md)
- [Streaming](client/streaming.md)
- [Async Usage](client/async-usage.md)

### 🚀 Deployment
Deploy ChoreoAI to production environments.
- [Deployment Overview](deployment/README.md)
- [Docker](deployment/docker.md)
- [Kubernetes](deployment/kubernetes.md)
- [Helm](deployment/helm.md)
- [Configuration](deployment/configuration.md)
- [Monitoring](deployment/monitoring.md)

### 🔌 Providers
Configure and use different AI providers.
- [Providers Overview](providers/README.md)
- [OpenAI](providers/openai.md)
- [Claude (Anthropic)](providers/claude.md)
- [Azure OpenAI](providers/azure-openai.md)
- [Google Gemini](providers/gemini.md)

### 💡 Examples & Tutorials
Practical guides and code examples.
- [Examples Overview](examples/README.md)
- [Basic Usage](examples/basic-usage.md)
- [Multi-Provider Setup](examples/multi-provider.md)
- [Fallback Strategy](examples/fallback-strategy.md)
- [Cost Optimization](examples/cost-optimization.md)

### 📖 Reference
Complete reference documentation.
- [Environment Variables](reference/environment-vars.md)
- [Error Codes](reference/error-codes.md)
- [Glossary](reference/glossary.md)
- [FAQ](reference/faq.md)

### 🔧 Development
Contributing and developing ChoreoAI.
- [Development Overview](development/README.md)
- [Local Setup](development/setup.md)
- [Project Structure](development/project-structure.md)
- [Adding Providers](development/adding-providers.md)
- [Testing](development/testing.md)
- [Contributing](development/contributing.md)

## Getting Started

New to ChoreoAI? Start here:

1. **[Installation](client/installation.md)** - Install the Python client
2. **[Quick Start](client/quickstart.md)** - Your first API call in 5 minutes
3. **[Authentication](api/authentication.md)** - Set up API keys
4. **[Providers](providers/README.md)** - Choose and configure your AI provider

## Community & Support

- **GitHub**: [github.com/choreoai](https://github.com/choreoai)
- **Issues**: Report bugs and request features on GitHub Issues
- **Discussions**: Join the conversation on GitHub Discussions

## License

ChoreoAI is open source software. See the LICENSE file for details.

---

**Ready to get started?** Jump to the [Quick Start Guide](client/quickstart.md) or explore the [API Reference](api/README.md).
