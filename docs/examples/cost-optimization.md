# Cost Optimization Strategies

This guide provides practical strategies for optimizing costs when using ChoreoAI with multiple AI providers.

## Table of Contents

- [Overview](#overview)
- [Provider Cost Comparison](#provider-cost-comparison)
- [Model Selection Strategies](#model-selection-strategies)
- [Token Optimization](#token-optimization)
- [Caching Strategies](#caching-strategies)
- [Rate Limiting](#rate-limiting)
- [Provider Fallback](#provider-fallback)
- [Monitoring Costs](#monitoring-costs)
- [Best Practices](#best-practices)

## Overview

AI API costs can add up quickly in production. This guide covers strategies to optimize costs while maintaining quality:

- **Smart Model Selection** - Choose the right model for each task
- **Token Management** - Reduce unnecessary token usage
- **Caching** - Avoid redundant API calls
- **Provider Selection** - Use cost-effective providers
- **Monitoring** - Track and control spending

## Provider Cost Comparison

### Cost per 1M Tokens (as of January 2024)

| Provider | Model | Input Cost | Output Cost | Best For |
|----------|-------|-----------|-------------|----------|
| **OpenAI** | GPT-4 Turbo | $10.00 | $30.00 | Complex reasoning |
| **OpenAI** | GPT-3.5 Turbo | $0.50 | $1.50 | General tasks |
| **Claude** | Claude 3.5 Sonnet | $3.00 | $15.00 | Balanced performance |
| **Claude** | Claude 3 Haiku | $0.25 | $1.25 | Fast, cheap tasks |
| **Gemini** | Gemini Pro | $0.50 | $1.50 | Cost-effective |
| **Azure OpenAI** | GPT-4 Turbo | $10.00 | $30.00 | Enterprise |

### Cost Comparison Example

```python
def calculate_cost(provider, model, input_tokens, output_tokens):
    """Calculate estimated API cost"""
    pricing = {
        "openai": {
            "gpt-4-turbo": {"input": 10, "output": 30},
            "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
        },
        "claude": {
            "claude-3-5-sonnet-20241022": {"input": 3, "output": 15},
            "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
        },
        "gemini": {
            "gemini-pro": {"input": 0.5, "output": 1.5},
        }
    }

    rates = pricing[provider][model]
    cost = (input_tokens * rates["input"] + output_tokens * rates["output"]) / 1_000_000

    return cost

# Example: 1000 input tokens, 500 output tokens
input_tokens, output_tokens = 1000, 500

print("Cost comparison for same task:")
print(f"GPT-4 Turbo: ${calculate_cost('openai', 'gpt-4-turbo', input_tokens, output_tokens):.4f}")
print(f"GPT-3.5 Turbo: ${calculate_cost('openai', 'gpt-3.5-turbo', input_tokens, output_tokens):.4f}")
print(f"Claude Sonnet: ${calculate_cost('claude', 'claude-3-5-sonnet-20241022', input_tokens, output_tokens):.4f}")
print(f"Claude Haiku: ${calculate_cost('claude', 'claude-3-haiku-20240307', input_tokens, output_tokens):.4f}")
print(f"Gemini Pro: ${calculate_cost('gemini', 'gemini-pro', input_tokens, output_tokens):.4f}")
```

Output:
```
Cost comparison for same task:
GPT-4 Turbo: $0.0250
GPT-3.5 Turbo: $0.0013
Claude Sonnet: $0.0105
Claude Haiku: $0.0009
Gemini Pro: $0.0013
```

## Model Selection Strategies

### Task-Based Model Selection

```python
from choreoai import ChoreoAI

class SmartModelSelector:
    """Automatically select the most cost-effective model for each task"""

    def __init__(self, api_key):
        self.client = ChoreoAI(api_key=api_key)
        self.model_map = {
            "simple": "claude-3-haiku-20240307",      # Cheapest
            "general": "gpt-3.5-turbo",               # Balanced
            "complex": "claude-3-5-sonnet-20241022",  # Smart but affordable
            "advanced": "gpt-4-turbo"                 # Most capable
        }

    def classify_task(self, prompt):
        """Classify task complexity based on prompt characteristics"""
        prompt_lower = prompt.lower()

        # Simple tasks
        simple_keywords = ["summarize", "translate", "list", "extract", "simple"]
        if any(kw in prompt_lower for kw in simple_keywords) and len(prompt) < 500:
            return "simple"

        # Complex tasks
        complex_keywords = ["analyze", "reason", "complex", "detailed", "comprehensive"]
        if any(kw in prompt_lower for kw in complex_keywords):
            return "complex"

        # Advanced tasks
        advanced_keywords = ["research", "multi-step", "critical", "expert"]
        if any(kw in prompt_lower for kw in advanced_keywords):
            return "advanced"

        return "general"

    def chat(self, messages, **kwargs):
        """Automatically select model based on task complexity"""
        # Classify based on last user message
        user_messages = [m for m in messages if m["role"] == "user"]
        last_message = user_messages[-1]["content"] if user_messages else ""

        complexity = self.classify_task(last_message)
        model = self.model_map[complexity]

        print(f"Selected {model} for {complexity} task")

        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

# Usage
selector = SmartModelSelector(api_key="your-api-key")

# Simple task - uses Haiku (cheapest)
response = selector.chat([
    {"role": "user", "content": "Summarize this article in 3 bullet points"}
])

# Complex task - uses Sonnet (balanced)
response = selector.chat([
    {"role": "user", "content": "Analyze the architectural patterns in this codebase and suggest improvements"}
])

# Advanced task - uses GPT-4 (most capable)
response = selector.chat([
    {"role": "user", "content": "Conduct expert-level research on quantum computing algorithms"}
])
```

### Length-Based Model Selection

```python
def select_model_by_length(prompt_length, output_length):
    """Select model based on expected input/output length"""

    # Short tasks - use cheaper models
    if prompt_length < 500 and output_length < 500:
        return "claude-3-haiku-20240307"

    # Medium tasks - use balanced models
    elif prompt_length < 2000 and output_length < 1000:
        return "gpt-3.5-turbo"

    # Long tasks - use capable but affordable models
    elif prompt_length < 10000:
        return "claude-3-5-sonnet-20241022"

    # Very long tasks - use models with large context
    else:
        return "claude-3-5-sonnet-20241022"  # 200K context

# Usage
prompt = "Your prompt here..."
expected_output = 500  # tokens

model = select_model_by_length(len(prompt), expected_output)
```

## Token Optimization

### 1. Limit Output Tokens

```python
# Bad - no limit, potentially wasteful
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": "Summarize this article"}]
)

# Good - set appropriate max_tokens
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": "Summarize this article in 100 words"}],
    max_tokens=150  # Limit output
)
```

### 2. Optimize Prompts

```python
# Bad - verbose prompt
prompt = """
I would like you to please help me understand what this code does.
Could you explain it to me in detail? I'm particularly interested in
understanding how it works and what each part does. Please be thorough.
"""

# Good - concise prompt
prompt = "Explain this code's functionality:"

# Even better - specific prompt
prompt = "Explain this code in 50 words:"
```

### 3. Remove Unnecessary Context

```python
def optimize_conversation_history(messages, max_history=5):
    """Keep only recent messages to reduce token usage"""

    # Always keep system message
    system_messages = [m for m in messages if m["role"] == "system"]
    other_messages = [m for m in messages if m["role"] != "system"]

    # Keep only last N messages
    recent_messages = other_messages[-max_history:]

    return system_messages + recent_messages

# Usage
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    # ... many messages ...
    {"role": "user", "content": "What's the weather?"},
]

optimized = optimize_conversation_history(messages, max_history=5)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=optimized  # Fewer tokens
)
```

### 4. Compress Long Documents

```python
def chunk_and_summarize(document, chunk_size=2000):
    """Summarize long documents in chunks to reduce tokens"""

    # Split into chunks
    chunks = [document[i:i+chunk_size] for i in range(0, len(document), chunk_size)]

    summaries = []
    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Cheap model for summaries
            messages=[
                {"role": "user", "content": f"Summarize in 2 sentences:\n\n{chunk}"}
            ],
            max_tokens=100
        )
        summaries.append(response.choices[0].message.content)

    # Final summary of summaries
    combined = "\n".join(summaries)
    final_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Create final summary:\n\n{combined}"}
        ],
        max_tokens=200
    )

    return final_response.choices[0].message.content
```

## Caching Strategies

### 1. Response Caching

```python
import hashlib
import json
from functools import lru_cache

class CachedChoreoAI:
    """ChoreoAI client with response caching"""

    def __init__(self, api_key, cache_size=1000):
        self.client = ChoreoAI(api_key=api_key)
        self.cache = {}
        self.cache_size = cache_size

    def _get_cache_key(self, model, messages, **kwargs):
        """Generate cache key from request parameters"""
        cache_data = {
            "model": model,
            "messages": messages,
            **kwargs
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()

    def chat(self, model, messages, use_cache=True, **kwargs):
        """Chat with caching support"""
        if not use_cache:
            return self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )

        cache_key = self._get_cache_key(model, messages, **kwargs)

        # Check cache
        if cache_key in self.cache:
            print("Cache hit - saving API cost!")
            return self.cache[cache_key]

        # Make API call
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

        # Store in cache
        if len(self.cache) >= self.cache_size:
            # Remove oldest entry
            self.cache.pop(next(iter(self.cache)))

        self.cache[cache_key] = response
        return response

# Usage
cached_client = CachedChoreoAI(api_key="your-api-key")

# First call - API request
response1 = cached_client.chat(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What is Python?"}]
)

# Second identical call - cached, no cost!
response2 = cached_client.chat(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What is Python?"}]
)
```

### 2. Redis Caching

```python
import redis
import json

class RedisCachedClient:
    """ChoreoAI client with Redis caching for distributed systems"""

    def __init__(self, api_key, redis_host="localhost", redis_port=6379, ttl=3600):
        self.client = ChoreoAI(api_key=api_key)
        self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.ttl = ttl  # Cache TTL in seconds

    def _get_cache_key(self, model, messages):
        cache_data = json.dumps({"model": model, "messages": messages}, sort_keys=True)
        return f"choreoai:{hashlib.md5(cache_data.encode()).hexdigest()}"

    def chat(self, model, messages, **kwargs):
        cache_key = self._get_cache_key(model, messages)

        # Check Redis cache
        cached = self.redis.get(cache_key)
        if cached:
            print("Redis cache hit!")
            return json.loads(cached)

        # Make API call
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

        # Store in Redis with TTL
        self.redis.setex(
            cache_key,
            self.ttl,
            json.dumps(response.model_dump())
        )

        return response
```

## Rate Limiting

### Request Rate Limiting

```python
import time
from collections import deque

class RateLimitedClient:
    """Client with built-in rate limiting to control costs"""

    def __init__(self, api_key, max_requests_per_minute=60):
        self.client = ChoreoAI(api_key=api_key)
        self.max_requests = max_requests_per_minute
        self.requests = deque()

    def _wait_if_needed(self):
        """Implement sliding window rate limit"""
        now = time.time()

        # Remove requests older than 1 minute
        while self.requests and self.requests[0] < now - 60:
            self.requests.popleft()

        # Wait if at limit
        if len(self.requests) >= self.max_requests:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                print(f"Rate limit reached. Waiting {sleep_time:.1f}s...")
                time.sleep(sleep_time)
                self._wait_if_needed()  # Retry

        self.requests.append(now)

    def chat(self, model, messages, **kwargs):
        self._wait_if_needed()
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
```

### Budget Limiting

```python
class BudgetLimitedClient:
    """Client with cost tracking and budget limits"""

    def __init__(self, api_key, daily_budget=10.0):
        self.client = ChoreoAI(api_key=api_key)
        self.daily_budget = daily_budget
        self.today_spend = 0.0
        self.last_reset = time.time()

    def _reset_if_new_day(self):
        """Reset daily spend at midnight"""
        if time.time() - self.last_reset > 86400:  # 24 hours
            self.today_spend = 0.0
            self.last_reset = time.time()

    def _estimate_cost(self, model, usage):
        """Estimate cost from usage"""
        pricing = {
            "gpt-4-turbo": {"input": 10, "output": 30},
            "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
            "claude-3-5-sonnet-20241022": {"input": 3, "output": 15},
        }

        rates = pricing.get(model, {"input": 3, "output": 15})
        cost = (
            usage.prompt_tokens * rates["input"] +
            usage.completion_tokens * rates["output"]
        ) / 1_000_000

        return cost

    def chat(self, model, messages, **kwargs):
        self._reset_if_new_day()

        # Check budget
        if self.today_spend >= self.daily_budget:
            raise Exception(f"Daily budget of ${self.daily_budget} exceeded!")

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

        # Track cost
        cost = self._estimate_cost(model, response.usage)
        self.today_spend += cost

        print(f"Request cost: ${cost:.4f} | Today: ${self.today_spend:.2f}/{self.daily_budget}")

        return response
```

## Provider Fallback

### Cost-Optimized Fallback

```python
class CostOptimizedClient:
    """Fallback to cheaper providers when possible"""

    def __init__(self, api_key):
        self.client = ChoreoAI(api_key=api_key)
        self.provider_preference = [
            ("claude", "claude-3-haiku-20240307"),      # Cheapest
            ("gemini", "gemini-pro"),                    # Cheap
            ("openai", "gpt-3.5-turbo"),                # Moderate
            ("claude", "claude-3-5-sonnet-20241022"),   # Good value
            ("openai", "gpt-4-turbo"),                  # Most expensive
        ]

    def chat(self, messages, min_quality="cheap", **kwargs):
        """Try providers in cost order"""
        quality_index = {
            "cheap": 0,
            "moderate": 2,
            "high": 3,
            "best": 4
        }

        start_index = quality_index.get(min_quality, 0)

        for provider, model in self.provider_preference[start_index:]:
            try:
                print(f"Trying {provider}/{model}...")
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    **kwargs
                )
                print(f"Success with {model}")
                return response
            except Exception as e:
                print(f"Failed with {model}: {e}")
                continue

        raise Exception("All providers failed")

# Usage
client = CostOptimizedClient(api_key="your-api-key")

# Will try cheapest models first
response = client.chat(
    messages=[{"role": "user", "content": "What is AI?"}],
    min_quality="cheap"
)

# Will skip cheap models and start at high quality
response = client.chat(
    messages=[{"role": "user", "content": "Complex analysis required"}],
    min_quality="high"
)
```

## Monitoring Costs

### Cost Tracking

```python
import sqlite3
from datetime import datetime

class CostTracker:
    """Track API costs over time"""

    def __init__(self, db_path="costs.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS api_costs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                provider TEXT,
                model TEXT,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cost REAL
            )
        """)
        self.conn.commit()

    def log_request(self, provider, model, usage, cost):
        """Log a request cost"""
        self.conn.execute("""
            INSERT INTO api_costs (timestamp, provider, model, input_tokens, output_tokens, cost)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            provider,
            model,
            usage.prompt_tokens,
            usage.completion_tokens,
            cost
        ))
        self.conn.commit()

    def get_daily_cost(self):
        """Get today's total cost"""
        cursor = self.conn.execute("""
            SELECT SUM(cost) FROM api_costs
            WHERE DATE(timestamp) = DATE('now')
        """)
        return cursor.fetchone()[0] or 0.0

    def get_monthly_cost(self):
        """Get this month's total cost"""
        cursor = self.conn.execute("""
            SELECT SUM(cost) FROM api_costs
            WHERE strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
        """)
        return cursor.fetchone()[0] or 0.0

    def get_cost_by_provider(self):
        """Get costs broken down by provider"""
        cursor = self.conn.execute("""
            SELECT provider, SUM(cost) as total_cost
            FROM api_costs
            WHERE DATE(timestamp) >= DATE('now', '-30 days')
            GROUP BY provider
            ORDER BY total_cost DESC
        """)
        return cursor.fetchall()
```

## Best Practices

### 1. Use Appropriate Models

```python
# Don't use GPT-4 for simple tasks
# Bad
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": "What's 2+2?"}]
)

# Good - use cheaper model for simple tasks
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What's 2+2?"}]
)
```

### 2. Batch Requests

```python
# Bad - multiple separate requests
summaries = []
for article in articles:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Summarize: {article}"}]
    )
    summaries.append(response.choices[0].message.content)

# Good - batch in single request
combined_prompt = "\n\n---\n\n".join([f"Article {i+1}: {a}" for i, a in enumerate(articles)])
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{
        "role": "user",
        "content": f"Summarize each article in one sentence:\n\n{combined_prompt}"
    }]
)
```

### 3. Set Budget Alerts

```python
def check_budget_alert(spent, budget, threshold=0.8):
    """Alert when approaching budget"""
    if spent >= budget * threshold:
        print(f"⚠️  WARNING: {spent/budget*100:.1f}% of budget used!")
        # Send alert email, Slack message, etc.
```

### 4. Monitor and Optimize

```python
# Regularly analyze usage
tracker = CostTracker()

print(f"Today's cost: ${tracker.get_daily_cost():.2f}")
print(f"Monthly cost: ${tracker.get_monthly_cost():.2f}")
print(f"\nCost by provider:")
for provider, cost in tracker.get_cost_by_provider():
    print(f"  {provider}: ${cost:.2f}")
```

## Complete Example

```python
from choreoai import ChoreoAI
from functools import lru_cache
import hashlib
import json

class OptimizedClient:
    """Fully optimized client with caching, rate limiting, and cost tracking"""

    def __init__(self, api_key, daily_budget=10.0):
        self.client = ChoreoAI(api_key=api_key)
        self.cache = {}
        self.daily_budget = daily_budget
        self.today_spend = 0.0
        self.tracker = CostTracker()

    def _select_model(self, prompt):
        """Select most cost-effective model"""
        if len(prompt) < 500:
            return "claude-3-haiku-20240307"
        elif "complex" in prompt.lower() or "analyze" in prompt.lower():
            return "claude-3-5-sonnet-20241022"
        else:
            return "gpt-3.5-turbo"

    def _get_cache_key(self, model, messages):
        cache_str = json.dumps({"model": model, "messages": messages}, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()

    def _estimate_cost(self, model, usage):
        pricing = {
            "gpt-4-turbo": {"input": 10, "output": 30},
            "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
            "claude-3-5-sonnet-20241022": {"input": 3, "output": 15},
            "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
        }
        rates = pricing.get(model, {"input": 3, "output": 15})
        return (usage.prompt_tokens * rates["input"] + usage.completion_tokens * rates["output"]) / 1_000_000

    def chat(self, messages, model=None, use_cache=True, **kwargs):
        """Optimized chat with all cost-saving features"""

        # Auto-select model if not specified
        if not model:
            user_msg = [m["content"] for m in messages if m["role"] == "user"][-1]
            model = self._select_model(user_msg)

        # Check cache
        cache_key = self._get_cache_key(model, messages)
        if use_cache and cache_key in self.cache:
            print("✓ Cache hit - $0.00")
            return self.cache[cache_key]

        # Check budget
        if self.today_spend >= self.daily_budget:
            raise Exception(f"Daily budget exceeded: ${self.today_spend:.2f}/${self.daily_budget}")

        # Make request
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

        # Track cost
        cost = self._estimate_cost(model, response.usage)
        self.today_spend += cost
        self.tracker.log_request(
            provider=model.split("-")[0],
            model=model,
            usage=response.usage,
            cost=cost
        )

        print(f"✓ Request: ${cost:.4f} | Today: ${self.today_spend:.2f}/{self.daily_budget}")

        # Cache response
        if use_cache:
            self.cache[cache_key] = response

        return response

# Usage
client = OptimizedClient(api_key="your-api-key", daily_budget=5.0)

response = client.chat([
    {"role": "user", "content": "What is Python?"}
])
```

## Summary

Key cost optimization strategies:

1. **Select appropriate models** - Use cheaper models for simple tasks
2. **Limit tokens** - Set max_tokens and optimize prompts
3. **Cache responses** - Avoid redundant API calls
4. **Monitor spending** - Track costs and set budgets
5. **Use fallbacks** - Try cheaper providers first
6. **Batch requests** - Combine multiple requests when possible
7. **Compress context** - Remove unnecessary conversation history

## Additional Resources

- [Provider Pricing Comparison](../providers/README.md)
- [Multi-Provider Setup](multi-provider.md)
- [Fallback Strategies](fallback-strategy.md)
- [API Reference](../api/README.md)
