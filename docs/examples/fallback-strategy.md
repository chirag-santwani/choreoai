# Fallback Strategy Guide

Build resilient AI applications with intelligent fallback mechanisms. Learn how to handle provider outages, rate limits, and failures gracefully.

## Table of Contents

1. [Overview](#overview)
2. [Why Fallback Matters](#why-fallback-matters)
3. [Basic Fallback Implementation](#basic-fallback-implementation)
4. [Advanced Fallback Strategies](#advanced-fallback-strategies)
5. [Retry Logic](#retry-logic)
6. [Circuit Breaker Pattern](#circuit-breaker-pattern)
7. [Best Practices](#best-practices)
8. [Monitoring and Alerts](#monitoring-and-alerts)

## Overview

Fallback strategies ensure your application continues working even when:
- Primary AI provider is down
- Rate limits are exceeded
- Specific models are unavailable
- Network issues occur

### Key Concepts

**Primary Provider**: Your preferred AI provider (e.g., OpenAI)
**Fallback Provider**: Alternative provider to use if primary fails (e.g., Claude)
**Graceful Degradation**: Maintaining service with alternative providers

## Why Fallback Matters

### Common Failure Scenarios

1. **Provider Outages**: Even major providers experience downtime
2. **Rate Limiting**: Exceeding API quotas
3. **Model Unavailability**: Specific models may be temporarily unavailable
4. **Network Issues**: Connection problems, timeouts
5. **Cost Limits**: Reaching budget caps

### Benefits of Fallback

- **High Availability**: 99.9%+ uptime even with provider issues
- **Cost Optimization**: Switch to cheaper alternatives when needed
- **Performance**: Route to faster providers during peak times
- **Flexibility**: Adapt to changing conditions automatically

## Basic Fallback Implementation

### Simple Sequential Fallback

Try providers in order until one succeeds:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

def get_completion_with_fallback(prompt: str, max_tokens: int = 150) -> str:
    """
    Try multiple providers in sequence.
    """
    # Define fallback chain: Primary -> Fallback 1 -> Fallback 2
    models = [
        "gpt-4",                      # Primary: Most capable
        "claude-3-sonnet-20240229",   # Fallback 1: Good alternative
        "gpt-3.5-turbo"               # Fallback 2: Fast and reliable
    ]

    messages = [{"role": "user", "content": prompt}]

    for model in models:
        try:
            print(f"Trying {model}...")

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                timeout=10  # 10 second timeout
            )

            print(f"Success with {model}")
            return response.choices[0].message.content

        except Exception as e:
            print(f"Failed with {model}: {e}")
            continue

    # All providers failed
    raise Exception("All providers failed")

# Usage
try:
    result = get_completion_with_fallback("Explain machine learning")
    print(f"\nResult: {result}")
except Exception as e:
    print(f"Error: {e}")
```

### Expected Output

```
Trying gpt-4...
Success with gpt-4

Result: Machine learning is a subset of artificial intelligence...
```

### With Logging

Add comprehensive logging for debugging:

```python
import logging
from choreoai import ChoreoAI
from typing import Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FallbackClient:
    """Client with built-in fallback logic."""

    def __init__(self, api_key: str, fallback_chain: List[str]):
        self.client = ChoreoAI(api_key=api_key)
        self.fallback_chain = fallback_chain

    def get_completion(
        self,
        prompt: str,
        max_tokens: int = 150,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Get completion with automatic fallback.
        """
        messages = [{"role": "user", "content": prompt}]

        for i, model in enumerate(self.fallback_chain):
            try:
                logger.info(f"Attempt {i+1}/{len(self.fallback_chain)}: Trying {model}")

                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    timeout=10
                )

                logger.info(f"Success with {model} (tokens: {response.usage.total_tokens})")
                return response.choices[0].message.content

            except Exception as e:
                logger.warning(f"Failed with {model}: {str(e)}")

                # If this was the last model, raise exception
                if i == len(self.fallback_chain) - 1:
                    logger.error("All fallback providers failed")
                    raise Exception("All providers failed")

                # Otherwise, continue to next model
                logger.info(f"Falling back to next provider...")

        return None

# Usage
fallback_client = FallbackClient(
    api_key="your-api-key",
    fallback_chain=[
        "gpt-4",
        "claude-3-sonnet-20240229",
        "gpt-3.5-turbo"
    ]
)

result = fallback_client.get_completion("What is Python?")
print(f"\nResult: {result}")
```

## Advanced Fallback Strategies

### Provider Health Tracking

Track provider health and skip unhealthy ones:

```python
from choreoai import ChoreoAI
from datetime import datetime, timedelta
from typing import Dict, List
import time

class HealthAwareFallback:
    """Fallback client that tracks provider health."""

    def __init__(self, api_key: str):
        self.client = ChoreoAI(api_key=api_key)
        self.provider_health: Dict[str, Dict] = {}

    def mark_failure(self, model: str):
        """Mark a provider as failed."""
        if model not in self.provider_health:
            self.provider_health[model] = {
                "failures": 0,
                "last_failure": None,
                "healthy": True
            }

        health = self.provider_health[model]
        health["failures"] += 1
        health["last_failure"] = datetime.now()

        # Mark as unhealthy if 3+ failures in last 5 minutes
        if health["failures"] >= 3:
            health["healthy"] = False
            print(f"Marking {model} as unhealthy")

    def mark_success(self, model: str):
        """Mark a provider as successful."""
        if model not in self.provider_health:
            self.provider_health[model] = {
                "failures": 0,
                "last_failure": None,
                "healthy": True
            }

        # Reset failure count on success
        self.provider_health[model]["failures"] = 0
        self.provider_health[model]["healthy"] = True

    def is_healthy(self, model: str) -> bool:
        """Check if a provider is healthy."""
        if model not in self.provider_health:
            return True

        health = self.provider_health[model]

        # If marked unhealthy, check if cooldown period has passed
        if not health["healthy"] and health["last_failure"]:
            cooldown = timedelta(minutes=5)
            if datetime.now() - health["last_failure"] > cooldown:
                print(f"Cooldown expired for {model}, marking as healthy")
                health["healthy"] = True
                health["failures"] = 0

        return health["healthy"]

    def get_completion(
        self,
        prompt: str,
        models: List[str],
        max_tokens: int = 150
    ) -> str:
        """
        Get completion with health-aware fallback.
        """
        messages = [{"role": "user", "content": prompt}]

        # Filter to only healthy providers
        healthy_models = [m for m in models if self.is_healthy(m)]

        if not healthy_models:
            print("No healthy providers available, trying all...")
            healthy_models = models

        for model in healthy_models:
            try:
                print(f"Trying {model}...")

                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    timeout=10
                )

                self.mark_success(model)
                print(f"Success with {model}")
                return response.choices[0].message.content

            except Exception as e:
                print(f"Failed with {model}: {e}")
                self.mark_failure(model)
                continue

        raise Exception("All providers failed")

# Usage
client = HealthAwareFallback(api_key="your-api-key")

models = [
    "gpt-4",
    "claude-3-sonnet-20240229",
    "gpt-3.5-turbo"
]

# Make multiple requests
for i in range(5):
    try:
        result = client.get_completion(
            f"Request {i+1}: Tell me a fact",
            models=models
        )
        print(f"Got result: {result[:50]}...\n")
    except Exception as e:
        print(f"All providers failed: {e}\n")

    time.sleep(1)
```

### Cost-Based Fallback

Prefer cheaper providers while maintaining quality:

```python
from choreoai import ChoreoAI
from typing import List, Dict, Tuple

# Cost per 1K tokens (approximate)
PROVIDER_COSTS = {
    "gpt-4": 0.03,
    "gpt-4-turbo": 0.01,
    "gpt-3.5-turbo": 0.002,
    "claude-3-opus-20240229": 0.015,
    "claude-3-sonnet-20240229": 0.003,
    "claude-3-haiku-20240307": 0.00025,
    "gemini-pro": 0.001
}

class CostOptimizedFallback:
    """Fallback client that optimizes for cost."""

    def __init__(self, api_key: str, budget_per_request: float = 0.01):
        self.client = ChoreoAI(api_key=api_key)
        self.budget_per_request = budget_per_request

    def get_affordable_models(
        self,
        models: List[str],
        estimated_tokens: int = 500
    ) -> List[str]:
        """
        Filter models by budget.
        """
        affordable = []

        for model in models:
            cost = PROVIDER_COSTS.get(model, 0.01)
            estimated_cost = (estimated_tokens / 1000) * cost

            if estimated_cost <= self.budget_per_request:
                affordable.append(model)

        # Sort by cost (cheapest first)
        affordable.sort(key=lambda m: PROVIDER_COSTS.get(m, 0.01))

        return affordable

    def get_completion(
        self,
        prompt: str,
        models: List[str],
        quality: str = "high"  # "high", "medium", "low"
    ) -> Tuple[str, float]:
        """
        Get completion optimizing for cost within quality tier.

        Returns:
            Tuple of (response, actual_cost)
        """
        # Estimate tokens (rough estimate)
        estimated_tokens = len(prompt.split()) * 2 + 150

        # Get affordable models
        affordable = self.get_affordable_models(models, estimated_tokens)

        if not affordable:
            print("No models within budget, trying all...")
            affordable = models

        # Organize by quality tier
        high_quality = ["gpt-4", "claude-3-opus-20240229"]
        medium_quality = ["gpt-4-turbo", "claude-3-sonnet-20240229"]
        low_quality = ["gpt-3.5-turbo", "claude-3-haiku-20240307", "gemini-pro"]

        # Select models based on quality preference
        if quality == "high":
            preferred = [m for m in affordable if m in high_quality]
            preferred += [m for m in affordable if m not in high_quality]
        elif quality == "medium":
            preferred = [m for m in affordable if m in medium_quality]
            preferred += [m for m in affordable if m not in medium_quality]
        else:
            preferred = [m for m in affordable if m in low_quality]
            preferred += [m for m in affordable if m not in low_quality]

        # Try providers
        messages = [{"role": "user", "content": prompt}]

        for model in preferred:
            try:
                print(f"Trying {model} (cost: ${PROVIDER_COSTS.get(model, 0.01):.4f}/1K tokens)...")

                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=150,
                    timeout=10
                )

                # Calculate actual cost
                tokens = response.usage.total_tokens
                cost = (tokens / 1000) * PROVIDER_COSTS.get(model, 0.01)

                print(f"Success with {model}: {tokens} tokens, ${cost:.4f}")

                return response.choices[0].message.content, cost

            except Exception as e:
                print(f"Failed with {model}: {e}")
                continue

        raise Exception("All providers failed")

# Usage
client = CostOptimizedFallback(
    api_key="your-api-key",
    budget_per_request=0.005  # $0.005 per request
)

models = [
    "gpt-4",
    "claude-3-sonnet-20240229",
    "gpt-3.5-turbo",
    "gemini-pro"
]

# High quality request
result, cost = client.get_completion(
    "Explain quantum computing",
    models=models,
    quality="high"
)
print(f"\nHigh quality result (${cost:.4f}): {result[:100]}...")

# Low budget request
result, cost = client.get_completion(
    "What is Python?",
    models=models,
    quality="low"
)
print(f"\nLow cost result (${cost:.4f}): {result[:100]}...")
```

## Retry Logic

### Exponential Backoff

Implement exponential backoff for transient failures:

```python
import time
from choreoai import ChoreoAI
from typing import Optional

class RetryableClient:
    """Client with retry logic."""

    def __init__(self, api_key: str):
        self.client = ChoreoAI(api_key=api_key)

    def get_completion_with_retry(
        self,
        model: str,
        prompt: str,
        max_retries: int = 3,
        base_delay: float = 1.0
    ) -> Optional[str]:
        """
        Get completion with exponential backoff retry.
        """
        messages = [{"role": "user", "content": prompt}]

        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries}...")

                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=150,
                    timeout=10
                )

                return response.choices[0].message.content

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")

                # If this was the last attempt, raise
                if attempt == max_retries - 1:
                    raise

                # Calculate exponential backoff delay
                delay = base_delay * (2 ** attempt)
                print(f"Waiting {delay:.1f} seconds before retry...")
                time.sleep(delay)

        return None

# Usage
client = RetryableClient(api_key="your-api-key")

try:
    result = client.get_completion_with_retry(
        model="gpt-4",
        prompt="What is AI?",
        max_retries=3,
        base_delay=1.0
    )
    print(f"\nSuccess: {result}")
except Exception as e:
    print(f"\nFailed after retries: {e}")
```

### Jittered Exponential Backoff

Add randomness to prevent thundering herd problem:

```python
import time
import random
from choreoai import ChoreoAI

def jittered_backoff(attempt: int, base_delay: float = 1.0, max_delay: float = 32.0) -> float:
    """
    Calculate delay with jitter.
    """
    # Exponential component
    delay = min(base_delay * (2 ** attempt), max_delay)

    # Add jitter (random component between 0 and delay)
    jittered_delay = delay * random.random()

    return jittered_delay

def get_completion_with_jitter(
    client: ChoreoAI,
    model: str,
    prompt: str,
    max_retries: int = 3
) -> str:
    """Get completion with jittered backoff."""

    messages = [{"role": "user", "content": prompt}]

    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}...")

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=150,
                timeout=10
            )

            return response.choices[0].message.content

        except Exception as e:
            if attempt == max_retries - 1:
                raise

            delay = jittered_backoff(attempt)
            print(f"Waiting {delay:.2f}s...")
            time.sleep(delay)

# Usage
client = ChoreoAI(api_key="your-api-key")
result = get_completion_with_jitter(client, "gpt-4", "Hello")
print(f"Result: {result}")
```

## Circuit Breaker Pattern

Prevent cascading failures with circuit breaker:

```python
from enum import Enum
from datetime import datetime, timedelta
from choreoai import ChoreoAI

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

class CircuitBreaker:
    """Circuit breaker for AI provider."""

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout_seconds: int = 60,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timedelta(seconds=timeout_seconds)
        self.half_open_max_calls = half_open_max_calls

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0

    def call(self, func, *args, **kwargs):
        """
        Execute function through circuit breaker.
        """
        # Check if circuit should transition from OPEN to HALF_OPEN
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.last_failure_time > self.timeout:
                print("Circuit transitioning to HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
            else:
                raise Exception("Circuit is OPEN, request rejected")

        # HALF_OPEN: Limit test calls
        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.half_open_max_calls:
                raise Exception("Circuit HALF_OPEN call limit exceeded")
            self.half_open_calls += 1

        # Try the function call
        try:
            result = func(*args, **kwargs)

            # Success
            if self.state == CircuitState.HALF_OPEN:
                print("Circuit recovered, transitioning to CLOSED")
                self.state = CircuitState.CLOSED
                self.failure_count = 0

            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            print(f"Failure {self.failure_count}/{self.failure_threshold}")

            # Check if threshold exceeded
            if self.failure_count >= self.failure_threshold:
                print("Circuit opening due to failures")
                self.state = CircuitState.OPEN

            raise e

class CircuitBreakerClient:
    """Client with circuit breaker per provider."""

    def __init__(self, api_key: str):
        self.client = ChoreoAI(api_key=api_key)
        self.breakers = {}

    def get_breaker(self, model: str) -> CircuitBreaker:
        """Get or create circuit breaker for model."""
        if model not in self.breakers:
            self.breakers[model] = CircuitBreaker(
                failure_threshold=3,
                timeout_seconds=30
            )
        return self.breakers[model]

    def get_completion(
        self,
        models: list,
        prompt: str
    ) -> str:
        """Get completion with circuit breaker per provider."""

        messages = [{"role": "user", "content": prompt}]

        for model in models:
            breaker = self.get_breaker(model)

            try:
                print(f"\nTrying {model} (circuit: {breaker.state.value})...")

                def make_request():
                    return self.client.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_tokens=150,
                        timeout=10
                    )

                response = breaker.call(make_request)
                print(f"Success with {model}")
                return response.choices[0].message.content

            except Exception as e:
                print(f"Failed: {e}")
                continue

        raise Exception("All providers failed")

# Usage
client = CircuitBreakerClient(api_key="your-api-key")

models = ["gpt-4", "claude-3-sonnet-20240229", "gpt-3.5-turbo"]

# Simulate multiple requests
for i in range(10):
    try:
        result = client.get_completion(models, f"Request {i+1}")
        print(f"Result: {result[:50]}...\n")
    except Exception as e:
        print(f"All failed: {e}\n")

    time.sleep(1)
```

## Best Practices

### 1. Define Clear Fallback Chains

```python
# Good: Clear prioritization
FALLBACK_CHAINS = {
    "high_quality": [
        "gpt-4",
        "claude-3-opus-20240229",
        "gpt-4-turbo"
    ],
    "balanced": [
        "gpt-4-turbo",
        "claude-3-sonnet-20240229",
        "gpt-3.5-turbo"
    ],
    "cost_optimized": [
        "gpt-3.5-turbo",
        "claude-3-haiku-20240307",
        "gemini-pro"
    ]
}
```

### 2. Set Appropriate Timeouts

```python
# Configure timeouts for different scenarios
TIMEOUTS = {
    "quick_response": 5,    # 5 seconds
    "standard": 15,         # 15 seconds
    "complex_task": 60      # 60 seconds
}

response = client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    timeout=TIMEOUTS["standard"]
)
```

### 3. Log All Fallback Events

```python
import logging

logger = logging.getLogger(__name__)

def log_fallback_event(
    primary_model: str,
    fallback_model: str,
    reason: str
):
    """Log fallback events for monitoring."""
    logger.warning(
        f"Fallback triggered: {primary_model} -> {fallback_model}. "
        f"Reason: {reason}"
    )

    # Could also send to monitoring service
    # metrics.increment("fallback.triggered")
```

### 4. Test Fallback Scenarios

```python
def test_fallback():
    """Test fallback chain."""
    client = FallbackClient(
        api_key="your-api-key",
        fallback_chain=["gpt-4", "claude-3-sonnet-20240229"]
    )

    # Test with all providers available
    result = client.get_completion("Test 1")
    assert result is not None

    # Simulate primary failure (would need mocking)
    # ...

test_fallback()
```

## Monitoring and Alerts

### Track Fallback Metrics

```python
from collections import defaultdict
from typing import Dict

class FallbackMetrics:
    """Track fallback statistics."""

    def __init__(self):
        self.requests_by_model = defaultdict(int)
        self.failures_by_model = defaultdict(int)
        self.fallback_events = []

    def record_request(self, model: str):
        """Record successful request."""
        self.requests_by_model[model] += 1

    def record_failure(self, model: str):
        """Record failed request."""
        self.failures_by_model[model] += 1

    def record_fallback(self, from_model: str, to_model: str):
        """Record fallback event."""
        self.fallback_events.append({
            "from": from_model,
            "to": to_model,
            "timestamp": datetime.now()
        })

    def get_stats(self) -> Dict:
        """Get statistics."""
        return {
            "total_requests": sum(self.requests_by_model.values()),
            "total_failures": sum(self.failures_by_model.values()),
            "total_fallbacks": len(self.fallback_events),
            "requests_by_model": dict(self.requests_by_model),
            "failures_by_model": dict(self.failures_by_model),
            "fallback_rate": len(self.fallback_events) / max(sum(self.requests_by_model.values()), 1)
        }

# Usage
metrics = FallbackMetrics()

# After requests...
stats = metrics.get_stats()
print(f"Fallback rate: {stats['fallback_rate']:.2%}")
print(f"Total fallbacks: {stats['total_fallbacks']}")
```

## Complete Example

Here's a production-ready fallback implementation:

```python
from choreoai import ChoreoAI
import logging
from typing import List, Optional
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionFallbackClient:
    """
    Production-ready client with:
    - Sequential fallback
    - Retry logic with exponential backoff
    - Health tracking
    - Metrics
    - Logging
    """

    def __init__(
        self,
        api_key: str,
        fallback_chain: List[str],
        max_retries: int = 2
    ):
        self.client = ChoreoAI(api_key=api_key)
        self.fallback_chain = fallback_chain
        self.max_retries = max_retries
        self.health = {}

    def get_completion(
        self,
        prompt: str,
        max_tokens: int = 150,
        temperature: float = 0.7
    ) -> str:
        """
        Get completion with full fallback logic.
        """
        messages = [{"role": "user", "content": prompt}]
        last_error = None

        for model in self.fallback_chain:
            # Skip if recently failed
            if not self._is_healthy(model):
                logger.info(f"Skipping unhealthy provider: {model}")
                continue

            # Try with retries
            for attempt in range(self.max_retries):
                try:
                    logger.info(f"Attempting {model} (try {attempt+1}/{self.max_retries})")

                    response = self.client.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        timeout=15
                    )

                    logger.info(f"Success with {model}")
                    self._mark_success(model)
                    return response.choices[0].message.content

                except Exception as e:
                    last_error = e
                    logger.warning(f"Attempt {attempt+1} failed: {e}")

                    if attempt < self.max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff

            # All retries failed for this model
            self._mark_failure(model)

        # All providers failed
        logger.error("All providers and retries exhausted")
        raise Exception(f"All providers failed. Last error: {last_error}")

    def _is_healthy(self, model: str) -> bool:
        """Check if provider is healthy."""
        if model not in self.health:
            return True

        health = self.health[model]
        if health["failures"] < 3:
            return True

        # Check cooldown
        cooldown = timedelta(minutes=5)
        if datetime.now() - health["last_failure"] > cooldown:
            self.health[model]["failures"] = 0
            return True

        return False

    def _mark_success(self, model: str):
        """Mark provider as successful."""
        if model in self.health:
            self.health[model]["failures"] = 0

    def _mark_failure(self, model: str):
        """Mark provider as failed."""
        if model not in self.health:
            self.health[model] = {"failures": 0, "last_failure": None}

        self.health[model]["failures"] += 1
        self.health[model]["last_failure"] = datetime.now()

# Usage
client = ProductionFallbackClient(
    api_key="your-api-key",
    fallback_chain=[
        "gpt-4",
        "claude-3-sonnet-20240229",
        "gpt-3.5-turbo"
    ],
    max_retries=2
)

try:
    result = client.get_completion(
        "Explain the concept of microservices",
        max_tokens=200
    )
    print(f"\nResult: {result}")
except Exception as e:
    print(f"\nFailed: {e}")
```

## Next Steps

- **Optimize costs**: See [Cost Optimization Guide](cost-optimization.md)
- **Monitor performance**: Set up dashboards and alerts
- **Test thoroughly**: Create test scenarios for all failure modes

## Summary

Effective fallback strategies ensure your AI applications remain available and reliable. Key takeaways:

- Always have multiple providers configured
- Implement retry logic with exponential backoff
- Track provider health and skip unhealthy ones
- Log all fallback events for monitoring
- Test fallback scenarios regularly
- Set appropriate timeouts
- Use circuit breakers for cascading failure prevention

With proper fallback implementation, you can achieve 99.9%+ availability even when individual providers experience issues.
