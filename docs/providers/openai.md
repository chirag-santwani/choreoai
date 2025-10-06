# OpenAI Provider Guide

This guide covers how to use OpenAI models through ChoreoAI, including setup, configuration, and best practices.

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Supported Models](#supported-models)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Rate Limits](#rate-limits)
- [Pricing](#pricing)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

OpenAI provides state-of-the-art language models including GPT-4, GPT-4 Turbo, and GPT-3.5 Turbo. ChoreoAI provides seamless integration with OpenAI's API while maintaining full compatibility with the OpenAI SDK.

### Key Features
- **Advanced Language Models**: GPT-4, GPT-4 Turbo, GPT-3.5 Turbo
- **Function Calling**: Execute functions based on model decisions
- **Streaming Responses**: Real-time response generation
- **Vision Capabilities**: GPT-4V for image understanding
- **Embeddings**: Text-to-vector conversion for semantic search

## Getting Started

### 1. Get Your API Key

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in to your account
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy and save your API key (starts with `sk-`)

**Important**: Keep your API key secure and never commit it to version control.

### 2. Set Up Environment

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=sk-proj-...your-key-here...
```

Or create a `.env` file:

```bash
# .env file
OPENAI_API_KEY=sk-proj-...your-key-here...
```

### 3. Make Your First Request

#### Using cURL
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "What is ChoreoAI?"}
    ]
  }'
```

#### Using Python
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-proj-...",
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What is ChoreoAI?"}
    ]
)

print(response.choices[0].message.content)
```

## Supported Models

### Chat Models

| Model | Context Window | Training Data | Best For |
|-------|---------------|---------------|----------|
| **gpt-4** | 8K tokens | Up to Sep 2021 | Complex reasoning, accuracy |
| **gpt-4-32k** | 32K tokens | Up to Sep 2021 | Long context tasks |
| **gpt-4-turbo** | 128K tokens | Up to Apr 2023 | Large context, cost-effective |
| **gpt-4-turbo-preview** | 128K tokens | Up to Apr 2023 | Latest features, testing |
| **gpt-4o** | 128K tokens | Up to Oct 2023 | Balanced speed & quality |
| **gpt-4o-mini** | 128K tokens | Up to Oct 2023 | Fast, cost-effective |
| **gpt-3.5-turbo** | 16K tokens | Up to Sep 2021 | Fast, cost-effective |
| **gpt-3.5-turbo-16k** | 16K tokens | Up to Sep 2021 | Extended context |

### Embedding Models

| Model | Dimensions | Use Case |
|-------|-----------|----------|
| **text-embedding-3-small** | 1536 | Cost-effective embeddings |
| **text-embedding-3-large** | 3072 | High-quality embeddings |
| **text-embedding-ada-002** | 1536 | Legacy embeddings |

### Vision Models

| Model | Capabilities |
|-------|-------------|
| **gpt-4-vision-preview** | Image understanding, OCR, visual reasoning |
| **gpt-4-turbo** | Vision + enhanced performance |

## Configuration

### Basic Configuration

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="http://localhost:8000/v1"
)
```

### Advanced Configuration

```python
client = OpenAI(
    api_key="your-api-key",
    base_url="http://localhost:8000/v1",
    timeout=30.0,  # Request timeout in seconds
    max_retries=3  # Automatic retry attempts
)
```

### Environment Variables

```bash
# Required
export OPENAI_API_KEY=sk-proj-...

# Optional
export OPENAI_BASE_URL=http://localhost:8000/v1
export OPENAI_TIMEOUT=30
export OPENAI_MAX_RETRIES=3
```

## Usage Examples

### Basic Chat Completion

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### Streaming Responses

```python
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Write a short story"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Function Calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Boston?"}],
    tools=tools,
    tool_choice="auto"
)

# Handle function call
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    # Execute your function here
```

### Text Embeddings

```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="ChoreoAI is a unified API orchestration platform"
)

embedding = response.data[0].embedding
print(f"Embedding dimensions: {len(embedding)}")
```

### Vision (GPT-4V)

```python
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg"
                    }
                }
            ]
        }
    ],
    max_tokens=300
)

print(response.choices[0].message.content)
```

### Multi-turn Conversation

```python
messages = [
    {"role": "system", "content": "You are a helpful coding assistant."}
]

# First turn
messages.append({"role": "user", "content": "What is a closure in JavaScript?"})
response = client.chat.completions.create(model="gpt-4", messages=messages)
messages.append({"role": "assistant", "content": response.choices[0].message.content})

# Second turn
messages.append({"role": "user", "content": "Can you show me an example?"})
response = client.chat.completions.create(model="gpt-4", messages=messages)
print(response.choices[0].message.content)
```

### Adjusting Parameters

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write creative content"}],
    temperature=0.9,          # Creativity (0-2, default: 1)
    top_p=0.9,               # Nucleus sampling (0-1, default: 1)
    max_tokens=1000,         # Maximum response length
    frequency_penalty=0.5,    # Reduce repetition (-2 to 2, default: 0)
    presence_penalty=0.5,     # Encourage new topics (-2 to 2, default: 0)
    n=1,                     # Number of completions
    stop=["\n\n"]           # Stop sequences
)
```

## Rate Limits

OpenAI rate limits vary by usage tier:

### Free Tier (Trial)
- **RPM** (Requests Per Minute): 3
- **TPM** (Tokens Per Minute): 40,000
- **RPD** (Requests Per Day): 200

### Tier 1 ($5+ spent)
- **RPM**: 500
- **TPM**: 60,000
- **RPD**: Unlimited

### Tier 2 ($50+ spent)
- **RPM**: 5,000
- **TPM**: 450,000
- **RPD**: Unlimited

### Tier 3 ($100+ spent)
- **RPM**: 10,000
- **TPM**: 1,000,000
- **RPD**: Unlimited

### Tier 4 ($250+ spent)
- **RPM**: 30,000
- **TPM**: 5,000,000
- **RPD**: Unlimited

### Handling Rate Limits

```python
import time
from openai import RateLimitError

def chat_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
```

## Pricing

### Chat Models (as of 2024)

| Model | Input Price | Output Price |
|-------|------------|-------------|
| GPT-4 Turbo | $10 / 1M tokens | $30 / 1M tokens |
| GPT-4 | $30 / 1M tokens | $60 / 1M tokens |
| GPT-4 32K | $60 / 1M tokens | $120 / 1M tokens |
| GPT-4o | $5 / 1M tokens | $15 / 1M tokens |
| GPT-4o Mini | $0.15 / 1M tokens | $0.60 / 1M tokens |
| GPT-3.5 Turbo | $0.50 / 1M tokens | $1.50 / 1M tokens |

### Embedding Models

| Model | Price |
|-------|-------|
| text-embedding-3-small | $0.02 / 1M tokens |
| text-embedding-3-large | $0.13 / 1M tokens |
| text-embedding-ada-002 | $0.10 / 1M tokens |

### Cost Estimation

```python
def estimate_cost(model, input_tokens, output_tokens):
    pricing = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    }

    rate = pricing.get(model, {"input": 0, "output": 0})
    cost = (input_tokens * rate["input"] + output_tokens * rate["output"]) / 1000
    return f"${cost:.4f}"

# Example
print(estimate_cost("gpt-4", 1000, 500))  # $0.0600
```

## Best Practices

### 1. Model Selection

```python
def select_openai_model(task_type):
    models = {
        "simple": "gpt-3.5-turbo",      # Fast, cheap
        "balanced": "gpt-4o",            # Good balance
        "complex": "gpt-4-turbo",        # Best quality
        "creative": "gpt-4",             # Most creative
        "long_context": "gpt-4-turbo"   # 128K context
    }
    return models.get(task_type, "gpt-4o")
```

### 2. Optimize Token Usage

```python
# Use max_tokens to control costs
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Summarize this..."}],
    max_tokens=150  # Limit response length
)

# Count tokens before sending
import tiktoken

def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
```

### 3. System Messages

```python
# Good: Clear instructions
messages = [
    {
        "role": "system",
        "content": "You are a Python expert. Provide code examples and explain concepts clearly."
    },
    {"role": "user", "content": "Explain list comprehensions"}
]

# Better: Specific constraints
messages = [
    {
        "role": "system",
        "content": "You are a Python expert. Provide concise answers with code examples. "
                   "Keep responses under 200 words."
    },
    {"role": "user", "content": "Explain list comprehensions"}
]
```

### 4. Temperature Settings

```python
# Deterministic tasks (temperature = 0)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Calculate 15% of 250"}],
    temperature=0  # Consistent output
)

# Creative tasks (temperature = 0.7-1.0)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a creative story"}],
    temperature=0.9  # More random/creative
)
```

### 5. Error Handling

```python
from openai import OpenAI, OpenAIError, APIError, RateLimitError

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError:
    print("Rate limit exceeded. Please wait.")
except APIError as e:
    print(f"API error: {e}")
except OpenAIError as e:
    print(f"OpenAI error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 6. Context Management

```python
# Sliding window for long conversations
def manage_context(messages, max_tokens=4000):
    total_tokens = sum(count_tokens(m["content"]) for m in messages)

    while total_tokens > max_tokens and len(messages) > 2:
        # Keep system message, remove oldest user/assistant pair
        if messages[1]["role"] == "user":
            messages.pop(1)  # Remove old user message
            if len(messages) > 1 and messages[1]["role"] == "assistant":
                messages.pop(1)  # Remove corresponding assistant message
        total_tokens = sum(count_tokens(m["content"]) for m in messages)

    return messages
```

## Troubleshooting

### Common Issues

#### 1. Invalid API Key
```
Error: Incorrect API key provided
```

**Solution**:
```bash
# Verify API key
echo $OPENAI_API_KEY

# Should start with sk-proj- or sk-
# Get new key from https://platform.openai.com/api-keys
```

#### 2. Rate Limit Exceeded
```
Error: Rate limit exceeded
```

**Solution**:
- Implement exponential backoff
- Reduce request frequency
- Upgrade to higher tier
- Check usage: https://platform.openai.com/usage

#### 3. Model Not Found
```
Error: The model 'gpt-5' does not exist
```

**Solution**:
```python
# List available models
models = client.models.list()
for model in models.data:
    print(model.id)
```

#### 4. Context Length Exceeded
```
Error: This model's maximum context length is 8192 tokens
```

**Solution**:
```python
# Use a model with larger context
model = "gpt-4-turbo"  # 128K tokens

# Or truncate messages
messages = manage_context(messages, max_tokens=7000)
```

#### 5. Timeout Errors
```
Error: Request timed out
```

**Solution**:
```python
client = OpenAI(
    api_key="your-key",
    timeout=60.0,  # Increase timeout
    max_retries=3
)
```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Or use httpx logging for detailed requests
import httpx
logging.getLogger("httpx").setLevel(logging.DEBUG)
```

## Monitoring Usage

### Track API Usage

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)

# Log usage
usage = response.usage
print(f"Prompt tokens: {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")

# Estimate cost
cost = (usage.prompt_tokens * 0.03 + usage.completion_tokens * 0.06) / 1000
print(f"Estimated cost: ${cost:.4f}")
```

### Usage Dashboard

Check your usage at: https://platform.openai.com/usage

## Additional Resources

- **OpenAI API Documentation**: https://platform.openai.com/docs
- **OpenAI Python SDK**: https://github.com/openai/openai-python
- **Pricing Calculator**: https://openai.com/pricing
- **Status Page**: https://status.openai.com
- **Community Forum**: https://community.openai.com
- **API Reference**: https://platform.openai.com/docs/api-reference

## Next Steps

- **[Try Claude Provider](claude.md)** - Explore Anthropic's models
- **[Streaming Guide](../api/streaming.md)** - Implement real-time responses
- **[Error Handling](../api/error-handling.md)** - Handle errors gracefully
- **[Examples](../examples/README.md)** - See more code examples
