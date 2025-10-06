# Python Client

Official Python SDK for ChoreoAI - a unified interface to multiple AI providers.

## Overview

The ChoreoAI Python client provides a simple, intuitive interface to interact with the ChoreoAI API. It supports both synchronous and asynchronous operations, streaming responses, and all major AI models.

## Key Features

- **🐍 Pythonic API** - Clean, idiomatic Python interface
- **🔄 Sync & Async** - Support for both synchronous and asynchronous code
- **⚡ Streaming** - Real-time response streaming
- **🔌 Multi-Provider** - Access OpenAI, Claude, Gemini, and Azure OpenAI
- **📝 Type Hints** - Full type annotation support
- **🛡️ Error Handling** - Comprehensive exception handling
- **🔑 Environment Variables** - Automatic API key detection

## Installation

```bash
pip install choreoai
```

### Requirements

- Python 3.9 or higher
- pip (Python package manager)

See [Installation Guide](installation.md) for detailed instructions.

## Quick Start

```python
from choreoai import ChoreoAI

# Initialize client
client = ChoreoAI(api_key="your-api-key")

# Create chat completion
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What is machine learning?"}
    ]
)

print(response.choices[0].message.content)
```

See [Quick Start Guide](quickstart.md) for a complete tutorial.

## Basic Usage

### Chat Completions

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing"}
    ],
    temperature=0.7,
    max_tokens=200
)

print(response.choices[0].message.content)
```

### Streaming Responses

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

### Async/Await

```python
from choreoai import AsyncChoreoAI
import asyncio

async def main():
    client = AsyncChoreoAI(api_key="your-api-key")

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )

    print(response.choices[0].message.content)

asyncio.run(main())
```

## API Reference

### ChoreoAI Client

```python
from choreoai import ChoreoAI

client = ChoreoAI(
    api_key="your-api-key",       # Optional: reads from CHOREOAI_API_KEY env var
    base_url="http://localhost:8000",  # Optional: default base URL
    timeout=30.0,                 # Optional: request timeout in seconds
    max_retries=2                 # Optional: number of retries on failure
)
```

### Chat Completions

```python
response = client.chat.completions.create(
    model="gpt-4",                # Required: model identifier
    messages=[...],               # Required: conversation messages
    temperature=0.7,              # Optional: 0.0 to 2.0
    max_tokens=None,              # Optional: max tokens to generate
    top_p=1.0,                    # Optional: nucleus sampling
    stream=False,                 # Optional: enable streaming
    stop=None,                    # Optional: stop sequences
    presence_penalty=0,           # Optional: -2.0 to 2.0
    frequency_penalty=0,          # Optional: -2.0 to 2.0
)
```

### Embeddings

```python
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Text to embed"
)

embedding = response.data[0].embedding
```

### Models

```python
# List all models
models = client.models.list()

# Get specific model
model = client.models.retrieve("gpt-4")
```

## Environment Variables

The client automatically reads configuration from environment variables:

```bash
# API Key
export CHOREOAI_API_KEY=your-api-key

# Base URL (optional)
export CHOREOAI_BASE_URL=http://localhost:8000
```

Then use the client without explicit configuration:

```python
from choreoai import ChoreoAI

client = ChoreoAI()  # Reads from environment variables
```

## Error Handling

```python
from choreoai import ChoreoAI
from choreoai.exceptions import (
    AuthenticationError,
    RateLimitError,
    APIError
)

client = ChoreoAI(api_key="your-api-key")

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded, please retry")
except APIError as e:
    print(f"API error: {e}")
```

## OpenAI Compatibility

The ChoreoAI client is designed to be compatible with the OpenAI Python SDK:

```python
# OpenAI SDK
import openai
openai.api_base = "http://localhost:8000/v1"
openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Documentation Sections

### Getting Started
- **[Installation](installation.md)** - Install the client
- **[Quick Start](quickstart.md)** - Your first request in 5 minutes

### Core Features
- **[Chat Completions](chat.md)** - Generate chat responses
- **[Streaming](streaming.md)** - Real-time streaming responses
- **[Async Usage](async-usage.md)** - Async/await patterns

### Advanced
- **[Error Handling](../api/error-handling.md)** - Handle errors gracefully
- **[Multi-Provider](../examples/multi-provider.md)** - Use multiple providers

## Examples

### Multi-Turn Conversation

```python
messages = []

# First message
messages.append({"role": "user", "content": "What is Python?"})
response = client.chat.completions.create(model="gpt-4", messages=messages)
messages.append({"role": "assistant", "content": response.choices[0].message.content})

# Follow-up
messages.append({"role": "user", "content": "What are its main uses?"})
response = client.chat.completions.create(model="gpt-4", messages=messages)

print(response.choices[0].message.content)
```

### Switch Providers

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

### Batch Processing

```python
questions = [
    "What is AI?",
    "What is ML?",
    "What is DL?"
]

for question in questions:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    print(f"Q: {question}")
    print(f"A: {response.choices[0].message.content}\n")
```

## Best Practices

### 1. Use Environment Variables

```python
# .env file
CHOREOAI_API_KEY=your-api-key

# Python code
from choreoai import ChoreoAI
from dotenv import load_dotenv

load_dotenv()
client = ChoreoAI()  # Automatically uses env var
```

### 2. Reuse Client Instances

```python
# Good: Create once, reuse
client = ChoreoAI(api_key="your-api-key")

for i in range(10):
    response = client.chat.completions.create(...)

# Bad: Create in loop
for i in range(10):
    client = ChoreoAI(api_key="your-api-key")
    response = client.chat.completions.create(...)
```

### 3. Handle Errors

```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    print(f"Error: {e}")
    # Implement retry or fallback logic
```

### 4. Use Async for Concurrency

```python
import asyncio
from choreoai import AsyncChoreoAI

async def process_multiple():
    client = AsyncChoreoAI()

    tasks = [
        client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": q}]
        )
        for q in questions
    ]

    responses = await asyncio.gather(*tasks)
    return responses
```

### 5. Set Appropriate Timeouts

```python
client = ChoreoAI(
    api_key="your-api-key",
    timeout=60.0  # 60 second timeout for long requests
)
```

## Next Steps

- **[Installation](installation.md)** - Install the Python client
- **[Quick Start](quickstart.md)** - Build your first app
- **[Chat Guide](chat.md)** - Master chat completions
- **[Streaming](streaming.md)** - Implement real-time streaming
- **[Async Usage](async-usage.md)** - Use async/await patterns
