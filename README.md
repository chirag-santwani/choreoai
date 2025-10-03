# ChoreoAI

A unified API orchestration platform for multiple AI providers.

## Features

- 🔄 Unified OpenAI-compatible API
- 🌐 Multiple provider support (OpenAI, Claude, Gemini, Grok, Azure, Bedrock)
- 🚀 FastAPI-based high-performance service
- 📦 Python client library for easy integration
- ☸️ Kubernetes-ready with Helm charts
- 🔒 Built-in authentication and rate limiting
- 📊 Monitoring and observability

## Quick Start

### Development Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `cd api && pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure
6. Run: `uvicorn app.main:app --reload`

### Using Docker Compose
```bash
docker-compose up
```
