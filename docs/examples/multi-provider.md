# Multi-Provider Guide

Learn how to use multiple AI providers seamlessly with ChoreoAI. Switch between OpenAI, Claude, Gemini, Grok, and more without changing your code.

## Table of Contents

1. [Overview](#overview)
2. [Supported Providers](#supported-providers)
3. [Quick Start](#quick-start)
4. [Provider-Specific Examples](#provider-specific-examples)
5. [Comparing Providers](#comparing-providers)
6. [Best Practices](#best-practices)
7. [Advanced Usage](#advanced-usage)

## Overview

ChoreoAI provides a unified OpenAI-compatible API for multiple AI providers. This means you can:

- Use the same code with different providers
- Switch providers by changing only the model name
- Compare responses from different models
- Build multi-model applications easily

### How It Works

```
Your Application
       ↓
  ChoreoAI API
       ↓
┌──────┼──────┬──────┬──────┐
↓      ↓      ↓      ↓      ↓
OpenAI Claude Gemini Grok  Azure
```

ChoreoAI automatically routes requests to the correct provider based on the model name.

## Supported Providers

### OpenAI
- **Models**: GPT-3.5 Turbo, GPT-4, GPT-4 Turbo, GPT-4o
- **Strengths**: Versatile, fast, well-documented
- **Best for**: General-purpose tasks, function calling

### Anthropic Claude
- **Models**: Claude 3 Haiku, Sonnet, Opus
- **Strengths**: Long context, careful reasoning
- **Best for**: Analysis, long documents, safety-critical tasks

### Google Gemini
- **Models**: Gemini Pro, Gemini Ultra
- **Strengths**: Multimodal, fast, cost-effective
- **Best for**: Multimodal tasks, high-throughput applications

### xAI Grok
- **Models**: Grok-1
- **Strengths**: Real-time information, creative
- **Best for**: Up-to-date information, creative tasks

### Azure OpenAI
- **Models**: All OpenAI models via Azure
- **Strengths**: Enterprise features, compliance
- **Best for**: Enterprise deployments, regulated industries

### AWS Bedrock
- **Models**: Various models via AWS
- **Strengths**: AWS integration, compliance
- **Best for**: AWS-native applications

## Quick Start

### Setup

First, configure your provider API keys:

```bash
# Set provider API keys
export OPENAI_API_KEY=sk-your-openai-key
export ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
export GOOGLE_API_KEY=your-google-key
export GROK_API_KEY=your-grok-key
```

### Basic Usage

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-choreoai-key")

# Use OpenAI
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(f"GPT-4: {response.choices[0].message.content}")

# Use Claude - same code, different model
response = client.chat.completions.create(
    model="claude-3-sonnet-20240229",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(f"Claude: {response.choices[0].message.content}")

# Use Gemini - same code, different model
response = client.chat.completions.create(
    model="gemini-pro",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(f"Gemini: {response.choices[0].message.content}")
```

### Expected Output

```
GPT-4: Hello! How can I assist you today?
Claude: Hello! How may I help you?
Gemini: Hello! What can I do for you?
```

## Provider-Specific Examples

### OpenAI GPT Models

OpenAI offers several models optimized for different use cases:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# GPT-3.5 Turbo - Fast and cost-effective
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in one sentence."}
    ]
)
print(f"GPT-3.5: {response.choices[0].message.content}")

# GPT-4 - More capable, better reasoning
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in one sentence."}
    ]
)
print(f"GPT-4: {response.choices[0].message.content}")

# GPT-4 Turbo - Faster GPT-4 with longer context
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in one sentence."}
    ]
)
print(f"GPT-4 Turbo: {response.choices[0].message.content}")
```

### Claude Models

Anthropic's Claude models are known for careful, nuanced responses:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Claude 3 Haiku - Fast and efficient
response = client.chat.completions.create(
    model="claude-3-haiku-20240307",
    messages=[
        {"role": "user", "content": "Write a haiku about artificial intelligence."}
    ],
    max_tokens=100
)
print(f"Haiku:\n{response.choices[0].message.content}")

# Claude 3 Sonnet - Balanced performance
response = client.chat.completions.create(
    model="claude-3-sonnet-20240229",
    messages=[
        {"role": "user", "content": "Analyze the pros and cons of renewable energy."}
    ],
    max_tokens=500
)
print(f"\nSonnet:\n{response.choices[0].message.content}")

# Claude 3 Opus - Most capable
response = client.chat.completions.create(
    model="claude-3-opus-20240229",
    messages=[
        {"role": "user", "content": "Explain the theory of relativity in detail."}
    ],
    max_tokens=1000
)
print(f"\nOpus:\n{response.choices[0].message.content}")
```

### Gemini Models

Google's Gemini models offer multimodal capabilities:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Gemini Pro - Versatile and fast
response = client.chat.completions.create(
    model="gemini-pro",
    messages=[
        {"role": "user", "content": "What are the key benefits of using AI?"}
    ]
)
print(f"Gemini Pro:\n{response.choices[0].message.content}")

# Gemini supports longer contexts
long_prompt = """
Analyze this business scenario:
A startup wants to build an e-commerce platform...
[Long detailed scenario]
"""

response = client.chat.completions.create(
    model="gemini-pro",
    messages=[
        {"role": "user", "content": long_prompt}
    ]
)
print(f"\nAnalysis:\n{response.choices[0].message.content}")
```

## Comparing Providers

### Side-by-Side Comparison

Compare responses from different providers for the same prompt:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Define the question
question = "What are the three laws of robotics?"

# Models to compare
models = [
    ("GPT-4", "gpt-4"),
    ("Claude 3 Sonnet", "claude-3-sonnet-20240229"),
    ("Gemini Pro", "gemini-pro")
]

# Get responses from each model
print("Comparing responses from different providers:")
print("=" * 60)

for name, model in models:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
        max_tokens=200
    )

    print(f"\n{name}:")
    print("-" * 60)
    print(response.choices[0].message.content)
    print(f"\nTokens used: {response.usage.total_tokens}")
```

### Expected Output

```
Comparing responses from different providers:
============================================================

GPT-4:
------------------------------------------------------------
The Three Laws of Robotics, formulated by Isaac Asimov:
1. A robot may not injure a human being or allow harm
2. A robot must obey human orders unless it conflicts with #1
3. A robot must protect its existence unless it conflicts with #1 or #2

Tokens used: 67

Claude 3 Sonnet:
------------------------------------------------------------
Isaac Asimov's Three Laws of Robotics are:
First Law: A robot may not injure a human being...
[Detailed explanation]

Tokens used: 89

Gemini Pro:
------------------------------------------------------------
The Three Laws of Robotics are principles created by...
[Concise explanation]

Tokens used: 54
```

### Comparison Function

Create a reusable comparison function:

```python
from choreoai import ChoreoAI
from typing import List, Dict

def compare_models(
    prompt: str,
    models: List[str],
    client: ChoreoAI
) -> Dict[str, Dict]:
    """
    Compare responses from multiple models.

    Args:
        prompt: The prompt to send to all models
        models: List of model names to compare
        client: ChoreoAI client instance

    Returns:
        Dictionary mapping model names to response data
    """
    results = {}

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )

            results[model] = {
                "content": response.choices[0].message.content,
                "tokens": response.usage.total_tokens,
                "model": response.model
            }
        except Exception as e:
            results[model] = {
                "error": str(e)
            }

    return results

# Usage
client = ChoreoAI(api_key="your-api-key")

results = compare_models(
    prompt="Explain machine learning in simple terms.",
    models=["gpt-3.5-turbo", "claude-3-haiku-20240307", "gemini-pro"],
    client=client
)

# Display results
for model, data in results.items():
    print(f"\n{model}:")
    print("-" * 60)
    if "error" in data:
        print(f"Error: {data['error']}")
    else:
        print(data["content"])
        print(f"\nTokens: {data['tokens']}")
```

## Best Practices

### 1. Choose the Right Model for the Task

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# For simple tasks: Use fast, cost-effective models
def simple_task(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Fast and cheap
        messages=[{"role": "user", "content": question}],
        max_tokens=100
    )
    return response.choices[0].message.content

# For complex reasoning: Use powerful models
def complex_task(problem: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",  # Better reasoning
        messages=[{"role": "user", "content": problem}],
        max_tokens=500,
        temperature=0.3  # More focused
    )
    return response.choices[0].message.content

# For long documents: Use high-context models
def analyze_document(document: str) -> str:
    response = client.chat.completions.create(
        model="claude-3-sonnet-20240229",  # 200k context
        messages=[{"role": "user", "content": f"Analyze: {document}"}],
        max_tokens=1000
    )
    return response.choices[0].message.content
```

### 2. Handle Provider-Specific Features

Some features vary by provider:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Function calling works best with OpenAI models
def use_function_calling():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"}
                    },
                    "required": ["location"]
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",  # OpenAI supports function calling well
        messages=[{"role": "user", "content": "What's the weather in NYC?"}],
        tools=tools
    )

    return response

# For Claude, focus on analysis and long context
def use_claude_strengths():
    long_text = "..." # Long document

    response = client.chat.completions.create(
        model="claude-3-opus-20240229",
        messages=[
            {
                "role": "user",
                "content": f"Provide a detailed analysis of:\n\n{long_text}"
            }
        ],
        max_tokens=2000
    )

    return response.choices[0].message.content
```

### 3. Implement Graceful Degradation

Fall back to alternative models if preferred one fails:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

def get_completion_with_fallback(prompt: str) -> str:
    """
    Try preferred model first, fall back to alternatives.
    """
    models = [
        "gpt-4",              # Preferred
        "claude-3-sonnet-20240229",  # Fallback 1
        "gpt-3.5-turbo"       # Fallback 2
    ]

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            print(f"Success with {model}")
            return response.choices[0].message.content

        except Exception as e:
            print(f"Failed with {model}: {e}")
            continue

    raise Exception("All models failed")

# Usage
result = get_completion_with_fallback("Explain photosynthesis")
print(result)
```

### 4. Monitor Costs Across Providers

```python
from choreoai import ChoreoAI
from typing import Dict

# Approximate costs per 1K tokens (input + output)
COSTS = {
    "gpt-3.5-turbo": 0.002,
    "gpt-4": 0.03,
    "gpt-4-turbo": 0.01,
    "claude-3-haiku-20240307": 0.00025,
    "claude-3-sonnet-20240229": 0.003,
    "claude-3-opus-20240229": 0.015,
    "gemini-pro": 0.001
}

def estimate_cost(model: str, tokens: int) -> float:
    """Estimate cost for a request."""
    rate = COSTS.get(model, 0.002)
    return (tokens / 1000) * rate

client = ChoreoAI(api_key="your-api-key")

# Track costs
total_cost = 0.0

models = ["gpt-3.5-turbo", "claude-3-haiku-20240307", "gemini-pro"]

for model in models:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Hello!"}]
    )

    tokens = response.usage.total_tokens
    cost = estimate_cost(model, tokens)
    total_cost += cost

    print(f"{model}: {tokens} tokens, ${cost:.4f}")

print(f"\nTotal cost: ${total_cost:.4f}")
```

## Advanced Usage

### A/B Testing Different Models

```python
from choreoai import ChoreoAI
import random

class ModelABTest:
    """A/B test different models."""

    def __init__(self, client: ChoreoAI, model_a: str, model_b: str):
        self.client = client
        self.model_a = model_a
        self.model_b = model_b
        self.results = {"a": [], "b": []}

    def get_completion(self, prompt: str) -> Dict:
        """Get completion and track which model was used."""
        # Randomly choose model (50/50 split)
        use_a = random.random() < 0.5
        model = self.model_a if use_a else self.model_b
        variant = "a" if use_a else "b"

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        result = {
            "model": model,
            "content": response.choices[0].message.content,
            "tokens": response.usage.total_tokens
        }

        self.results[variant].append(result)

        return result

    def get_stats(self) -> Dict:
        """Get A/B test statistics."""
        return {
            "model_a": {
                "name": self.model_a,
                "requests": len(self.results["a"]),
                "avg_tokens": sum(r["tokens"] for r in self.results["a"]) / len(self.results["a"]) if self.results["a"] else 0
            },
            "model_b": {
                "name": self.model_b,
                "requests": len(self.results["b"]),
                "avg_tokens": sum(r["tokens"] for r in self.results["b"]) / len(self.results["b"]) if self.results["b"] else 0
            }
        }

# Usage
client = ChoreoAI(api_key="your-api-key")
ab_test = ModelABTest(client, "gpt-4", "claude-3-sonnet-20240229")

# Run tests
for i in range(10):
    result = ab_test.get_completion("Tell me a fun fact.")
    print(f"Request {i+1}: {result['model']}")

# View statistics
stats = ab_test.get_stats()
print(f"\nStatistics:")
print(f"Model A ({stats['model_a']['name']}): {stats['model_a']['requests']} requests")
print(f"Model B ({stats['model_b']['name']}): {stats['model_b']['requests']} requests")
```

### Dynamic Model Selection

```python
from choreoai import ChoreoAI
from typing import Optional

class SmartModelSelector:
    """Intelligently select model based on task characteristics."""

    def __init__(self, client: ChoreoAI):
        self.client = client

    def select_model(
        self,
        prompt: str,
        complexity: str = "medium",
        budget: str = "medium"
    ) -> str:
        """
        Select appropriate model based on task requirements.

        Args:
            prompt: The task prompt
            complexity: "low", "medium", or "high"
            budget: "low", "medium", or "high"

        Returns:
            Model name
        """
        # Decision matrix
        if complexity == "low":
            if budget == "low":
                return "gpt-3.5-turbo"
            return "claude-3-haiku-20240307"

        elif complexity == "medium":
            if budget == "low":
                return "gemini-pro"
            return "claude-3-sonnet-20240229"

        else:  # high complexity
            if budget == "low":
                return "gpt-4-turbo"
            return "gpt-4"

    def get_completion(
        self,
        prompt: str,
        complexity: str = "medium",
        budget: str = "medium"
    ) -> Dict:
        """Get completion with automatic model selection."""
        model = self.select_model(prompt, complexity, budget)

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "model": model,
            "content": response.choices[0].message.content,
            "tokens": response.usage.total_tokens
        }

# Usage
client = ChoreoAI(api_key="your-api-key")
selector = SmartModelSelector(client)

# Simple task, low budget
result = selector.get_completion(
    "What is 2+2?",
    complexity="low",
    budget="low"
)
print(f"Used {result['model']}: {result['content']}")

# Complex task, high budget
result = selector.get_completion(
    "Explain quantum entanglement in detail.",
    complexity="high",
    budget="high"
)
print(f"Used {result['model']}: {result['content'][:100]}...")
```

### List Available Models

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# List all available models
models = client.models.list()

# Categorize by provider
providers = {}
for model in models.data:
    if model.id.startswith("gpt-"):
        provider = "OpenAI"
    elif model.id.startswith("claude-"):
        provider = "Anthropic"
    elif model.id.startswith("gemini-"):
        provider = "Google"
    elif model.id.startswith("grok-"):
        provider = "xAI"
    else:
        provider = "Other"

    if provider not in providers:
        providers[provider] = []
    providers[provider].append(model.id)

# Display by provider
for provider, model_list in sorted(providers.items()):
    print(f"\n{provider} ({len(model_list)} models):")
    for model_id in sorted(model_list):
        print(f"  - {model_id}")
```

## Next Steps

- **Implement fallback strategies**: See [Fallback Strategy Guide](fallback-strategy.md)
- **Optimize costs**: See [Cost Optimization Guide](cost-optimization.md)
- **Learn advanced features**: See [API Documentation](../api/README.md)

## Troubleshooting

### Model Not Available

```python
# Check if a model is available
def is_model_available(client: ChoreoAI, model: str) -> bool:
    try:
        models = client.models.list()
        return any(m.id == model for m in models.data)
    except Exception as e:
        print(f"Error checking models: {e}")
        return False

if is_model_available(client, "gpt-4"):
    print("GPT-4 is available")
else:
    print("GPT-4 is not available")
```

### Provider API Key Issues

```python
# Test each provider
providers_to_test = {
    "OpenAI": "gpt-3.5-turbo",
    "Anthropic": "claude-3-haiku-20240307",
    "Google": "gemini-pro"
}

for provider, model in providers_to_test.items():
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )
        print(f"{provider}: OK")
    except Exception as e:
        print(f"{provider}: FAILED - {e}")
```

## Summary

With ChoreoAI's multi-provider support, you can:

- Use one API for all major AI providers
- Switch models without code changes
- Compare different models easily
- Optimize for cost and performance
- Build resilient multi-model applications

The key is choosing the right model for each task and implementing proper error handling and fallback mechanisms.
