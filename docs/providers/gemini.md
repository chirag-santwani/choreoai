# Google Gemini Provider Guide

This guide covers how to use Google's Gemini models through ChoreoAI, including setup, configuration, and best practices.

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

Google Gemini is Google's most capable AI model family, offering multimodal understanding, massive context windows, and competitive pricing. ChoreoAI will provide seamless integration with Gemini through an OpenAI-compatible interface.

### Key Features
- **Massive Context**: Up to 2 million tokens (Gemini 1.5 Pro)
- **Multimodal**: Native support for text, images, video, and audio
- **Free Tier**: Generous free usage limits
- **Low Latency**: Fast response times
- **Google Integration**: Seamless integration with Google Cloud

### Status
🚧 **Gemini integration is currently in development**

ChoreoAI's Gemini adapter is being developed. This documentation provides the planned implementation and configuration.

## Getting Started

### Prerequisites

1. **Google Account**: A Google account for API access
2. **API Key**: Gemini API key from Google AI Studio or Vertex AI

### 1. Get Your API Key

#### Option A: Google AI Studio (Recommended for Development)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy your API key

#### Option B: Vertex AI (Recommended for Production)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create or select a project
3. Enable Vertex AI API
4. Create a service account with Vertex AI permissions
5. Download service account key JSON

### 2. Set Up Environment

#### Using Google AI Studio API Key

```bash
export GEMINI_API_KEY=AIzaSy...your-key-here...
```

Or create a `.env` file:

```bash
# .env file
GEMINI_API_KEY=AIzaSy...your-key-here...
```

#### Using Vertex AI (Advanced)

```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
export GEMINI_LOCATION=us-central1
```

### 3. Make Your First Request (Coming Soon)

Once implemented, you'll be able to use Gemini like this:

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-gemini-api-key",
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[
        {"role": "user", "content": "What is ChoreoAI?"}
    ]
)

print(response.choices[0].message.content)
```

## Supported Models

### Gemini 1.5 Family (Latest)

| Model | Context Window | Strengths | Best For |
|-------|---------------|-----------|----------|
| **gemini-1.5-pro** | 2M tokens | Massive context, multimodal | Complex analysis, large documents |
| **gemini-1.5-flash** | 1M tokens | Fast, efficient | Quick responses, high volume |

### Gemini 1.0 Family (Legacy)

| Model | Context Window | Best For |
|-------|---------------|----------|
| **gemini-1.0-pro** | 32K tokens | General tasks |
| **gemini-1.0-pro-vision** | 16K tokens | Vision tasks |

### Model Comparison

| Feature | Gemini 1.5 Pro | Gemini 1.5 Flash | Gemini 1.0 Pro |
|---------|---------------|-----------------|----------------|
| Context Window | 2M tokens | 1M tokens | 32K tokens |
| Multimodal | ✅ Advanced | ✅ Basic | ❌ Text only* |
| Speed | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Cost | $$$ | $ | $$ |

*Gemini 1.0 Pro Vision supports images

### Context Window Sizes

Gemini 1.5 Pro's 2 million token context is groundbreaking:

- **2M tokens** ≈ 1.4M words
- Can process ~1,500 pages of text
- Can analyze hours of video/audio
- Entire codebases in a single context

## Configuration

### Basic Configuration (Planned)

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-gemini-api-key",
    base_url="http://localhost:8000/v1"
)
```

### Advanced Configuration (Planned)

```python
client = OpenAI(
    api_key="your-gemini-api-key",
    base_url="http://localhost:8000/v1",
    timeout=120.0,  # Longer timeout for large contexts
    max_retries=3
)
```

### Environment Variables

```bash
# Required (choose one)
export GEMINI_API_KEY=AIzaSy...                           # Google AI Studio
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json   # Vertex AI

# Optional
export GEMINI_BASE_URL=http://localhost:8000/v1
export GEMINI_MODEL=gemini-1.5-pro
export GOOGLE_CLOUD_PROJECT=your-project-id
export GEMINI_LOCATION=us-central1
```

## Usage Examples

### Basic Chat Completion (Planned)

```python
response = client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing"}
    ],
    temperature=0.7,
    max_tokens=1024
)

print(response.choices[0].message.content)
```

### Streaming Responses (Planned)

```python
stream = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[
        {"role": "user", "content": "Write a story about AI"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Vision - Image Understanding (Planned)

```python
response = client.chat.completions.create(
    model="gemini-1.5-pro",
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
    ]
)

print(response.choices[0].message.content)
```

### Long Context Analysis (Planned)

```python
# Analyze an entire book or codebase
with open("large_document.txt", "r") as f:
    document = f.read()  # Can be up to 2M tokens!

response = client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[
        {
            "role": "user",
            "content": f"Analyze this document and provide key insights:\n\n{document}"
        }
    ],
    max_tokens=4096
)

print(response.choices[0].message.content)
```

### Multi-turn Conversation (Planned)

```python
messages = [
    {"role": "system", "content": "You are a helpful coding assistant."}
]

# First turn
messages.append({"role": "user", "content": "Explain Python decorators"})
response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=messages
)
messages.append({"role": "assistant", "content": response.choices[0].message.content})

# Second turn
messages.append({"role": "user", "content": "Show me an example"})
response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=messages
)
print(response.choices[0].message.content)
```

### Video Analysis (Planned)

```python
# Gemini can analyze video content
response = client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Summarize this video"},
                {
                    "type": "video_url",
                    "video_url": {
                        "url": "https://example.com/video.mp4"
                    }
                }
            ]
        }
    ]
)
```

### Code Generation (Planned)

```python
response = client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[
        {
            "role": "user",
            "content": "Write a Python function to implement a binary search tree with insert, delete, and search operations"
        }
    ],
    temperature=0.3,  # Lower for more deterministic code
    max_tokens=2048
)

print(response.choices[0].message.content)
```

### JSON Mode (Planned)

```python
response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[
        {
            "role": "user",
            "content": """Extract information from this text as JSON:
            "Sarah Johnson, 35 years old, works as a data scientist at TechCorp in Seattle."

            Return format: {"name": "...", "age": ..., "occupation": "...", "company": "...", "location": "..."}"""
        }
    ],
    temperature=0
)

import json
result = json.loads(response.choices[0].message.content)
print(result)
```

### Adjusting Parameters (Planned)

```python
response = client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[{"role": "user", "content": "Write creative content"}],
    temperature=1.0,        # Creativity (0-2)
    top_p=0.95,            # Nucleus sampling
    top_k=40,              # Top-k sampling (Gemini-specific)
    max_tokens=2048,       # Maximum response length
    stop=["\n\n"]         # Stop sequences
)
```

## Rate Limits

### Google AI Studio (Free Tier)

| Model | RPM | TPM | RPD |
|-------|-----|-----|-----|
| Gemini 1.5 Pro | 2 | 32,000 | - |
| Gemini 1.5 Flash | 15 | 1,000,000 | - |
| Gemini 1.0 Pro | 15 | 1,000,000 | - |

### Google AI Studio (Paid Tier)

| Model | RPM | TPM |
|-------|-----|-----|
| Gemini 1.5 Pro | 1,000 | 4,000,000 |
| Gemini 1.5 Flash | 2,000 | 4,000,000 |

### Vertex AI

Vertex AI has different quotas based on your Google Cloud project:

- **Default Quota**: 300 RPM per model
- **Can Request Higher**: Up to several thousand RPM
- **Regional Quotas**: Quotas apply per region

### Handling Rate Limits (Planned)

```python
import time
from openai import RateLimitError

def chat_with_retry(messages, max_retries=5):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gemini-1.5-pro",
                messages=messages
            )
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = min(2 ** attempt, 60)  # Exponential backoff
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
```

## Pricing

### Google AI Studio Pricing

| Model | Input Price (per 1M tokens) | Output Price (per 1M tokens) |
|-------|---------------------------|----------------------------|
| **Gemini 1.5 Pro** | | |
| - Prompts ≤ 128K tokens | $1.25 | $5.00 |
| - Prompts > 128K tokens | $2.50 | $10.00 |
| **Gemini 1.5 Flash** | $0.075 | $0.30 |
| **Gemini 1.0 Pro** | $0.50 | $1.50 |

### Vertex AI Pricing (may vary by region)

| Model | Input Price (per 1M tokens) | Output Price (per 1M tokens) |
|-------|---------------------------|----------------------------|
| **Gemini 1.5 Pro** | | |
| - Prompts ≤ 128K tokens | $1.25 | $5.00 |
| - Prompts > 128K tokens | $2.50 | $10.00 |
| **Gemini 1.5 Flash** | $0.0375 | $0.15 |

### Free Tier (Google AI Studio)

- **Gemini 1.5 Flash**: 1,500 requests per day (free)
- **Gemini 1.5 Pro**: 50 requests per day (free)
- Perfect for development and testing

### Cost Estimation

```python
def estimate_gemini_cost(model, input_tokens, output_tokens):
    pricing = {
        "gemini-1.5-pro": {
            "input_small": 1.25,    # ≤128K tokens
            "input_large": 2.50,    # >128K tokens
            "output": 5.00
        },
        "gemini-1.5-flash": {
            "input": 0.075,
            "output": 0.30
        },
        "gemini-1.0-pro": {
            "input": 0.50,
            "output": 1.50
        }
    }

    if model == "gemini-1.5-pro":
        input_rate = pricing[model]["input_small"] if input_tokens <= 128000 else pricing[model]["input_large"]
        output_rate = pricing[model]["output"]
    else:
        rate = pricing.get(model, {"input": 0, "output": 0})
        input_rate = rate["input"]
        output_rate = rate.get("output", 0)

    cost = (input_tokens * input_rate + output_tokens * output_rate) / 1_000_000
    return f"${cost:.6f}"

# Example
print(estimate_gemini_cost("gemini-1.5-flash", 1000, 500))  # $0.000225
```

### Cost Comparison

Gemini is often more cost-effective:

```python
# Same task across providers
input_tokens = 10000
output_tokens = 2000

# Gemini 1.5 Flash
gemini_cost = (10000 * 0.075 + 2000 * 0.30) / 1_000_000  # $0.00135

# GPT-4 Turbo
gpt4_cost = (10000 * 10 + 2000 * 30) / 1_000_000        # $0.16000

# Claude 3.5 Sonnet
claude_cost = (10000 * 3 + 2000 * 15) / 1_000_000       # $0.06000

print(f"Gemini Flash: ${gemini_cost:.5f}")
print(f"GPT-4 Turbo: ${gpt4_cost:.5f}")
print(f"Claude Sonnet: ${claude_cost:.5f}")
```

## Best Practices

### 1. Model Selection

```python
def select_gemini_model(task_type, context_size):
    # For massive context (>100K tokens)
    if context_size > 100000:
        return "gemini-1.5-pro"

    # For speed-critical applications
    if task_type in ["simple", "fast"]:
        return "gemini-1.5-flash"

    # For complex reasoning with moderate context
    if task_type in ["complex", "analysis"]:
        return "gemini-1.5-pro"

    # Default to Flash for cost-effectiveness
    return "gemini-1.5-flash"
```

### 2. Leverage Massive Context

```python
# Gemini 1.5 Pro can handle entire codebases
def analyze_codebase(repo_path):
    files = []
    for root, dirs, filenames in os.walk(repo_path):
        for filename in filenames:
            if filename.endswith(('.py', '.js', '.java')):
                with open(os.path.join(root, filename)) as f:
                    files.append(f"File: {filename}\n{f.read()}")

    # Combine all files - can be massive!
    codebase = "\n\n".join(files)

    response = client.chat.completions.create(
        model="gemini-1.5-pro",
        messages=[
            {
                "role": "user",
                "content": f"Analyze this codebase for security vulnerabilities:\n\n{codebase}"
            }
        ]
    )
    return response.choices[0].message.content
```

### 3. Multimodal Capabilities

```python
# Combine text, images, and video
response = client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Compare these charts and explain the trends"},
                {"type": "image_url", "image_url": {"url": "https://example.com/chart1.png"}},
                {"type": "image_url", "image_url": {"url": "https://example.com/chart2.png"}},
            ]
        }
    ]
)
```

### 4. Temperature Settings

```python
# Factual tasks (temperature = 0)
response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    temperature=0  # Deterministic
)

# Creative tasks (temperature = 0.9-1.5)
response = client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[{"role": "user", "content": "Write a creative story"}],
    temperature=1.2  # More creative
)
```

### 5. Optimize for Speed

```python
# Use Flash for speed-critical applications
response = client.chat.completions.create(
    model="gemini-1.5-flash",  # Much faster than Pro
    messages=[{"role": "user", "content": "Quick question"}],
    max_tokens=150  # Limit output for faster response
)
```

### 6. Error Handling

```python
from openai import OpenAI, APIError, RateLimitError

try:
    response = client.chat.completions.create(
        model="gemini-1.5-pro",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError:
    print("Rate limit exceeded. Try Gemini Flash or wait.")
except APIError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 7. Prompt Engineering

Gemini responds well to structured prompts:

```python
# Good: Clear structure
prompt = """Task: Extract key insights from the following data.

Data:
{data}

Requirements:
- Identify top 3 trends
- Provide statistical evidence
- Suggest actionable recommendations

Format: Numbered list with supporting data"""

# Better: With examples
prompt = """Task: Extract key insights from the following data.

Example Output:
1. Trend: [description] (Evidence: [stats])
   Recommendation: [action]

Data:
{data}

Provide 3 insights in the format shown above."""
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
echo $GEMINI_API_KEY

# Should start with AIzaSy...
# Get new key from https://makersuite.google.com/app/apikey
```

#### 2. Model Not Available

```
Error: Model not found or not available
```

**Solution**:
- Verify model name: `gemini-1.5-pro`, `gemini-1.5-flash`
- Check regional availability
- Ensure API access is enabled

#### 3. Rate Limit Exceeded

```
Error: Rate limit exceeded
```

**Solution**:
- Use Gemini 1.5 Flash (higher free tier)
- Implement exponential backoff
- Upgrade to paid tier
- Switch to Vertex AI for higher quotas

#### 4. Context Too Long

```
Error: Input too long
```

**Solution**:
```python
# Gemini 1.5 Pro supports 2M tokens
# Ensure you're using the right model
model = "gemini-1.5-pro"  # Not gemini-1.0-pro (32K limit)

# Estimate tokens (rough: ~4 chars per token)
estimated_tokens = len(text) // 4
if estimated_tokens > 2_000_000:
    text = text[:2_000_000 * 4]  # Truncate
```

#### 5. Video/Image Processing Failed

```
Error: Failed to process media
```

**Solution**:
- Verify URL is publicly accessible
- Check file format (supported: JPEG, PNG, MP4, etc.)
- Ensure file size is within limits
- Use direct URLs, not redirects

### Debug Mode (Planned)

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# See full request/response
logging.getLogger("openai").setLevel(logging.DEBUG)
```

## Monitoring Usage

### Track API Usage (Planned)

```python
response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[{"role": "user", "content": "Hello"}]
)

# Log usage
usage = response.usage
print(f"Input tokens: {usage.prompt_tokens}")
print(f"Output tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")

# Estimate cost
cost = (usage.prompt_tokens * 0.075 + usage.completion_tokens * 0.30) / 1_000_000
print(f"Estimated cost: ${cost:.6f}")
```

### Usage Dashboard

- **Google AI Studio**: https://makersuite.google.com
- **Vertex AI Console**: https://console.cloud.google.com/vertex-ai

## Gemini-Specific Features

### 1. Massive Context Window

Gemini 1.5 Pro's 2M token context enables unique use cases:

```python
# Analyze entire books
# Process multi-hour videos
# Review complete codebases
# Analyze months of logs
```

### 2. Multimodal Understanding

Native support for multiple modalities:

```python
# Text + Images + Video + Audio in one request
# Cross-modal reasoning
# Visual question answering
```

### 3. Fast Inference

Gemini 1.5 Flash is optimized for speed:

```python
# Sub-second responses
# High throughput
# Perfect for real-time applications
```

### 4. Free Tier

Generous free tier for development:

```python
# 1,500 requests/day (Flash)
# 50 requests/day (Pro)
# No credit card required
```

## Additional Resources

- **Google AI Studio**: https://makersuite.google.com
- **Gemini API Documentation**: https://ai.google.dev/docs
- **Vertex AI Documentation**: https://cloud.google.com/vertex-ai/docs/generative-ai/learn/overview
- **Pricing**: https://ai.google.dev/pricing
- **Quickstart Guide**: https://ai.google.dev/tutorials/quickstart
- **Model Comparison**: https://ai.google.dev/models/gemini

## Next Steps

- **[OpenAI Provider](openai.md)** - Compare with OpenAI models
- **[Claude Provider](claude.md)** - Try Anthropic's models
- **[Provider Overview](README.md)** - Compare all providers
- **[API Reference](../api/README.md)** - Learn the API

---

**Note**: Gemini integration in ChoreoAI is currently under development. This documentation will be updated once the feature is available.
