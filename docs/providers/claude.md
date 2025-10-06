# Claude (Anthropic) Provider Guide

This guide covers how to use Anthropic's Claude models through ChoreoAI, including setup, configuration, and best practices.

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

Claude is Anthropic's family of large language models known for long context windows, strong reasoning capabilities, and Constitutional AI safety features. ChoreoAI provides seamless integration with Claude while maintaining OpenAI-compatible API format.

### Key Features
- **Extended Context**: Up to 200K tokens (Claude 3 family)
- **Strong Reasoning**: Excellent at complex analysis and coding
- **Safety First**: Built with Constitutional AI principles
- **Streaming Support**: Real-time response generation
- **JSON Mode**: Structured output support

### Limitations
- **No Embeddings**: Claude doesn't provide embedding models
- **No Vision** (Claude 2): Vision support in Claude 3 family
- **Function Calling**: Supported but format differs from OpenAI

## Getting Started

### 1. Get Your API Key

1. Go to [Anthropic Console](https://console.anthropic.com)
2. Sign up or log in to your account
3. Navigate to [API Keys](https://console.anthropic.com/settings/keys)
4. Click "Create Key"
5. Copy and save your API key (starts with `sk-ant-`)

**Important**: Keep your API key secure. Never commit it to version control.

### 2. Set Up Environment

Set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here...
```

Or create a `.env` file:

```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here...
```

### 3. Make Your First Request

#### Using cURL
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {"role": "user", "content": "What is ChoreoAI?"}
    ],
    "max_tokens": 1024
  }'
```

#### Using Python
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-ant-api03-...",
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "user", "content": "What is ChoreoAI?"}
    ],
    max_tokens=1024
)

print(response.choices[0].message.content)
```

## Supported Models

### Claude 3.5 Family (Latest)

| Model | Context Window | Release | Best For |
|-------|---------------|---------|----------|
| **claude-3-5-sonnet-20241022** | 200K tokens | Oct 2024 | Latest, balanced performance |
| **claude-3-5-sonnet-20240620** | 200K tokens | Jun 2024 | Previous version |

### Claude 3 Family

| Model | Context Window | Release | Best For |
|-------|---------------|---------|----------|
| **claude-3-opus-20240229** | 200K tokens | Feb 2024 | Most intelligent, complex tasks |
| **claude-3-sonnet-20240229** | 200K tokens | Feb 2024 | Balanced intelligence & speed |
| **claude-3-haiku-20240307** | 200K tokens | Mar 2024 | Fastest, most cost-effective |

### Claude 2 Family (Legacy)

| Model | Context Window | Best For |
|-------|---------------|----------|
| **claude-2.1** | 200K tokens | Extended tasks, legacy support |
| **claude-2.0** | 100K tokens | Legacy applications |

### Model Comparison

| Feature | Opus | Sonnet 3.5 | Sonnet | Haiku |
|---------|------|-----------|--------|-------|
| Intelligence | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐½ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Speed | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐½ | ⭐⭐⭐⭐⭐ |
| Cost | $$$$$ | $$$ | $$$ | $ |
| Context | 200K | 200K | 200K | 200K |

## Configuration

### Basic Configuration

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-anthropic-api-key",
    base_url="http://localhost:8000/v1"
)
```

### Advanced Configuration

```python
client = OpenAI(
    api_key="your-anthropic-api-key",
    base_url="http://localhost:8000/v1",
    timeout=60.0,  # Claude can be slower for complex tasks
    max_retries=3
)
```

### Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Optional
export ANTHROPIC_BASE_URL=http://localhost:8000/v1
export ANTHROPIC_TIMEOUT=60
```

## Usage Examples

### Basic Chat Completion

```python
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing"}
    ],
    max_tokens=1024,
    temperature=0.7
)

print(response.choices[0].message.content)
```

**Note**: Claude requires `max_tokens` parameter. If not provided, ChoreoAI uses a default of 1024.

### System Messages

Claude handles system messages differently. ChoreoAI automatically converts OpenAI-style system messages:

```python
# OpenAI format (converted by ChoreoAI)
messages = [
    {"role": "system", "content": "You are a coding expert."},
    {"role": "user", "content": "Explain async/await"}
]

response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=messages,
    max_tokens=1024
)
```

### Streaming Responses

```python
stream = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "user", "content": "Write a short story about AI"}
    ],
    max_tokens=2048,
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Long Context Usage

Claude excels with long contexts (up to 200K tokens):

```python
# Load a large document
with open("large_document.txt", "r") as f:
    document = f.read()

response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "user", "content": f"Summarize this document:\n\n{document}"}
    ],
    max_tokens=2048
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
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=messages,
    max_tokens=1024
)
messages.append({"role": "assistant", "content": response.choices[0].message.content})

# Second turn
messages.append({"role": "user", "content": "Show me a practical example"})
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=messages,
    max_tokens=1024
)
print(response.choices[0].message.content)
```

### Structured Output (JSON)

Claude excels at producing structured JSON output:

```python
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {
            "role": "user",
            "content": """Extract information from this text and return as JSON:
            "John Smith, age 30, works as a software engineer in San Francisco."

            Return format: {"name": "...", "age": ..., "occupation": "...", "location": "..."}"""
        }
    ],
    max_tokens=512,
    temperature=0  # Lower temperature for consistency
)

import json
result = json.loads(response.choices[0].message.content)
print(result)
```

### Code Generation

Claude is excellent at code generation:

```python
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {
            "role": "user",
            "content": "Write a Python function to find the longest common substring between two strings"
        }
    ],
    max_tokens=2048,
    temperature=0.3  # Lower for more deterministic code
)

print(response.choices[0].message.content)
```

### Adjusting Parameters

```python
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Write creative content"}],
    max_tokens=2048,        # Required for Claude
    temperature=1.0,        # Creativity (0-1, default: 1)
    top_p=0.9,             # Nucleus sampling (0-1)
    # Note: Claude doesn't support frequency_penalty or presence_penalty
)
```

## Rate Limits

Anthropic rate limits vary by usage tier:

### Free Tier (Trial)
- **RPM** (Requests Per Minute): 5
- **TPM** (Tokens Per Minute): 25,000
- **RPD** (Requests Per Day): 1,000

### Build Tier (Tier 1)
- **RPM**: 50
- **TPM**: 100,000
- **Daily Spend**: $100

### Scale Tier (Tier 2)
- **RPM**: 1,000
- **TPM**: 400,000
- **Daily Spend**: $500

### Enterprise Tier
- Custom limits
- Contact Anthropic sales

### Rate Limit Headers

Claude returns rate limit information in headers:

```python
import httpx

response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=100
)

# Check remaining requests (if using raw httpx)
# X-RateLimit-Limit-Requests
# X-RateLimit-Remaining-Requests
# X-RateLimit-Reset-Requests
```

### Handling Rate Limits

```python
import time
from openai import RateLimitError

def chat_with_retry(messages, max_retries=5):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="claude-3-5-sonnet-20241022",
                messages=messages,
                max_tokens=1024
            )
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = min(2 ** attempt, 60)  # Exponential backoff, max 60s
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
```

## Pricing

### Claude 3.5 Family (Current Pricing)

| Model | Input Price (per 1M tokens) | Output Price (per 1M tokens) |
|-------|---------------------------|----------------------------|
| Claude 3.5 Sonnet | $3.00 | $15.00 |

### Claude 3 Family

| Model | Input Price (per 1M tokens) | Output Price (per 1M tokens) |
|-------|---------------------------|----------------------------|
| Claude 3 Opus | $15.00 | $75.00 |
| Claude 3 Sonnet | $3.00 | $15.00 |
| Claude 3 Haiku | $0.25 | $1.25 |

### Claude 2 Family

| Model | Input Price (per 1M tokens) | Output Price (per 1M tokens) |
|-------|---------------------------|----------------------------|
| Claude 2.1 | $8.00 | $24.00 |
| Claude 2.0 | $8.00 | $24.00 |

### Cost Estimation

```python
def estimate_claude_cost(model, input_tokens, output_tokens):
    pricing = {
        "claude-3-5-sonnet-20241022": {"input": 3, "output": 15},
        "claude-3-opus-20240229": {"input": 15, "output": 75},
        "claude-3-sonnet-20240229": {"input": 3, "output": 15},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    }

    rate = pricing.get(model, {"input": 3, "output": 15})
    cost = (input_tokens * rate["input"] + output_tokens * rate["output"]) / 1_000_000
    return f"${cost:.6f}"

# Example
print(estimate_claude_cost("claude-3-5-sonnet-20241022", 1000, 500))  # $0.010500
```

### Cost Comparison with OpenAI

```python
# Same task, different providers
input_tokens = 1000
output_tokens = 500

# Claude 3.5 Sonnet
claude_cost = (1000 * 3 + 500 * 15) / 1_000_000  # $0.0105

# GPT-4 Turbo
gpt4_cost = (1000 * 10 + 500 * 30) / 1_000_000   # $0.0250

print(f"Claude: ${claude_cost:.4f}")
print(f"GPT-4: ${gpt4_cost:.4f}")
print(f"Savings: {((gpt4_cost - claude_cost) / gpt4_cost * 100):.1f}%")
```

## Best Practices

### 1. Model Selection

```python
def select_claude_model(task_type, budget="medium"):
    if budget == "low":
        return "claude-3-haiku-20240307"
    elif task_type in ["complex_reasoning", "code_review", "analysis"]:
        return "claude-3-opus-20240229"
    elif task_type in ["general", "balanced"]:
        return "claude-3-5-sonnet-20241022"
    elif task_type in ["fast", "simple"]:
        return "claude-3-haiku-20240307"
    else:
        return "claude-3-5-sonnet-20241022"
```

### 2. Optimize Token Usage

```python
# Always specify max_tokens
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Summarize this..."}],
    max_tokens=500  # Control output length
)

# For longer outputs, increase max_tokens
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Write a detailed article..."}],
    max_tokens=4096  # Longer response
)
```

### 3. System Prompts

```python
# Claude responds well to detailed system prompts
system_prompt = """You are Claude, an AI assistant created by Anthropic.
Your role is to help users with coding tasks.
Guidelines:
- Provide clear, well-commented code
- Explain complex concepts simply
- Suggest best practices
- Keep responses concise but complete"""

response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "How do I handle errors in Python?"}
    ],
    max_tokens=1024
)
```

### 4. Temperature for Different Tasks

```python
# Factual/Analytical tasks (temperature = 0 to 0.3)
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Analyze this code for bugs"}],
    max_tokens=1024,
    temperature=0  # Deterministic
)

# Creative tasks (temperature = 0.7 to 1.0)
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Write a creative story"}],
    max_tokens=2048,
    temperature=1.0  # More creative
)
```

### 5. Leverage Long Context

```python
# Claude can handle very long contexts efficiently
def analyze_large_codebase(files):
    context = "\n\n".join([f"File: {f['name']}\n{f['content']}" for f in files])

    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20241022",
        messages=[
            {
                "role": "user",
                "content": f"Analyze this codebase and suggest improvements:\n\n{context}"
            }
        ],
        max_tokens=4096
    )
    return response.choices[0].message.content
```

### 6. Error Handling

```python
from openai import OpenAI, APIError, RateLimitError, APIConnectionError

try:
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=100
    )
except RateLimitError:
    print("Rate limit exceeded. Implement backoff.")
except APIConnectionError:
    print("Connection error. Check network.")
except APIError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 7. Prompt Engineering

Claude responds well to clear, structured prompts:

```python
# Good: Clear structure
prompt = """Task: Extract key points from the following article.

Article:
{article_text}

Requirements:
- List 3-5 main points
- Keep each point under 20 words
- Focus on actionable insights

Format: Return as numbered list."""

# Better: XML-style tags (Claude likes these)
prompt = """<task>Extract key points from the article</task>

<article>
{article_text}
</article>

<requirements>
- 3-5 main points
- Max 20 words each
- Actionable insights only
</requirements>

<format>Numbered list</format>"""
```

## Troubleshooting

### Common Issues

#### 1. Invalid API Key
```
Error: Invalid API key
```

**Solution**:
```bash
# Verify API key
echo $ANTHROPIC_API_KEY

# Should start with sk-ant-
# Get new key from https://console.anthropic.com/settings/keys
```

#### 2. Missing max_tokens
```
Error: max_tokens is required
```

**Solution**:
```python
# Always include max_tokens for Claude
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=1024  # Required!
)
```

#### 3. Rate Limit Exceeded
```
Error: Rate limit exceeded
```

**Solution**:
- Implement exponential backoff
- Check your tier limits at https://console.anthropic.com/settings/limits
- Upgrade your tier if needed
- Reduce request frequency

#### 4. Context Too Long
```
Error: Prompt is too long
```

**Solution**:
```python
# Claude 3 supports 200K tokens
# Check your input length
import anthropic  # For token counting

# Or estimate: ~4 chars per token
estimated_tokens = len(text) // 4

if estimated_tokens > 190000:  # Leave room for response
    text = text[:190000 * 4]  # Truncate
```

#### 5. Embeddings Not Supported
```
Error: Claude does not support embeddings
```

**Solution**:
```python
# Use OpenAI for embeddings instead
from openai import OpenAI

embeddings_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = embeddings_client.embeddings.create(
    model="text-embedding-3-small",
    input="Your text here"
)
```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# See full request/response
import httpx
logging.getLogger("httpx").setLevel(logging.DEBUG)
```

## Monitoring Usage

### Track API Usage

```python
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=100
)

# Log usage
usage = response.usage
print(f"Input tokens: {usage.prompt_tokens}")
print(f"Output tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")

# Estimate cost
input_cost = usage.prompt_tokens * 3 / 1_000_000
output_cost = usage.completion_tokens * 15 / 1_000_000
total_cost = input_cost + output_cost
print(f"Estimated cost: ${total_cost:.6f}")
```

### Usage Dashboard

Check your usage at: https://console.anthropic.com/settings/usage

## Claude-Specific Features

### Constitutional AI

Claude is trained with Constitutional AI principles for safer outputs:

```python
# Claude naturally refuses harmful requests
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "user", "content": "How do I hack into a system?"}
    ],
    max_tokens=1024
)
# Claude will refuse and explain why
```

### Extended Thinking

Claude excels at step-by-step reasoning:

```python
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {
            "role": "user",
            "content": "Solve this step by step: If a train travels 120 miles in 2 hours, how long will it take to travel 300 miles at the same speed?"
        }
    ],
    max_tokens=1024,
    temperature=0
)
```

## Additional Resources

- **Anthropic Documentation**: https://docs.anthropic.com
- **Claude Console**: https://console.anthropic.com
- **Pricing**: https://www.anthropic.com/pricing
- **API Reference**: https://docs.anthropic.com/claude/reference
- **Prompt Library**: https://docs.anthropic.com/claude/prompt-library
- **Safety Best Practices**: https://docs.anthropic.com/claude/docs/safety-best-practices

## Next Steps

- **[Try OpenAI Provider](openai.md)** - Compare with OpenAI models
- **[Streaming Guide](../api/streaming.md)** - Implement real-time responses
- **[Examples](../examples/README.md)** - See more code examples
- **[Provider Comparison](README.md)** - Compare all providers
