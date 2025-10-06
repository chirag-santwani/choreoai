# Development Documentation

Welcome to the ChoreoAI development documentation. This guide will help you get started with developing, testing, and contributing to ChoreoAI.

## Overview

ChoreoAI is a unified API orchestration platform that provides a single OpenAI-compatible interface for multiple AI providers including OpenAI, Claude, Gemini, Grok, Azure OpenAI, and AWS Bedrock.

### Key Components

- **API Service**: FastAPI-based backend that handles routing and adapter orchestration
- **Python Client**: SDK for easy integration with Python applications
- **Adapters**: Provider-specific implementations that translate between OpenAI format and provider formats
- **Infrastructure**: Kubernetes, Helm, and Terraform configurations for deployment

## Documentation Structure

This development documentation is organized into the following sections:

### [Setup Guide](./setup.md)
Complete instructions for setting up your local development environment, including:
- Prerequisites and dependencies
- Virtual environment setup
- Running the API server
- Running the Python client
- Configuration management

### [Project Structure](./project-structure.md)
Detailed explanation of the codebase organization:
- Directory layout
- Module responsibilities
- File naming conventions
- Key architectural patterns

### [Adding Providers](./adding-providers.md)
Step-by-step guide for adding support for new AI providers:
- Implementing the BaseAdapter interface
- Message format conversion
- Testing your adapter
- Registering with the factory

### [Testing Guide](./testing.md)
Comprehensive testing documentation:
- Unit testing guidelines
- Integration testing
- Running the test suite
- Writing effective tests
- Test coverage requirements

### [Contributing Guidelines](./contributing.md)
How to contribute to ChoreoAI:
- Code style and standards
- Pull request process
- Commit message conventions
- Code review expectations
- Community guidelines

## Quick Links

- [Main README](../../README.md)
- [API Documentation](../api/README.md)
- [Client Documentation](../client/README.md)
- [Deployment Guide](../deployment/README.md)

## Getting Help

If you need help or have questions:

1. Check the relevant documentation section above
2. Review existing issues on GitHub
3. Join our community discussions
4. Open a new issue with the `question` label

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Client Applications                  │
│         (Using OpenAI SDK or ChoreoAI Client)           │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP/HTTPS
                     │
┌────────────────────▼────────────────────────────────────┐
│                    ChoreoAI API Gateway                  │
│                    (FastAPI Service)                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Routers: /chat, /embeddings, /models            │  │
│  └────────────┬─────────────────────────────────────┘  │
│               │                                          │
│  ┌────────────▼─────────────────────────────────────┐  │
│  │           Adapter Factory                        │  │
│  │  (Routes requests to appropriate adapter)        │  │
│  └────┬────┬────┬────┬────┬────┬─────────────────┬─┘  │
└───────┼────┼────┼────┼────┼────┼─────────────────┼────┘
        │    │    │    │    │    │                 │
   ┌────▼┐ ┌─▼──┐ ┌▼──┐ ┌──▼┐ ┌─▼──┐ ┌──▼───┐ ┌──▼───┐
   │OpenAI│ │Claude│ │Gemini│ │Grok│ │Azure│ │Bedrock│
   │Adapter│ │Adapter│ │Adapter│ │Adapter│ │Adapter│ │Adapter│
   └────┬┘ └─┬──┘ └┬──┘ └──┬┘ └─┬──┘ └──┬───┘ └──┬───┘
        │    │    │    │    │    │                 │
   ┌────▼────▼────▼────▼────▼────▼─────────────────▼────┐
   │              External AI Provider APIs               │
   │  OpenAI │ Anthropic │ Google │ xAI │ Azure │ AWS   │
   └──────────────────────────────────────────────────────┘
```

## Development Workflow

1. **Set up your environment** - Follow the [Setup Guide](./setup.md)
2. **Understand the codebase** - Review the [Project Structure](./project-structure.md)
3. **Make your changes** - Follow best practices and coding standards
4. **Write tests** - See [Testing Guide](./testing.md)
5. **Submit a PR** - Follow [Contributing Guidelines](./contributing.md)

## Key Technologies

- **Python 3.12+**: Primary programming language
- **FastAPI**: Web framework for the API service
- **Pydantic**: Data validation and settings management
- **httpx**: Async HTTP client
- **pytest**: Testing framework
- **Docker**: Containerization
- **Kubernetes**: Orchestration
- **Helm**: Kubernetes package manager

## Next Steps

1. Start with the [Setup Guide](./setup.md) to get your development environment running
2. Explore the [Project Structure](./project-structure.md) to understand the codebase
3. Check out the [Contributing Guidelines](./contributing.md) before making changes
