# Error Handling

Comprehensive guide to handling errors when using the ChoreoAI API.

## Error Response Format

All errors follow a consistent structure:

```json
{
  "error": {
    "message": "Human-readable error description",
    "type": "error_category",
    "code": "specific_error_code",
    "param": "parameter_name"  // Optional: which parameter caused the error
  }
}
```

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| 200 | OK | Request succeeded |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Invalid or missing API key |
| 403 | Forbidden | API key doesn't have required permissions |
| 404 | Not Found | Resource or endpoint not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 502 | Bad Gateway | Provider error or timeout |
| 503 | Service Unavailable | Service temporarily unavailable |

## Error Types

### Authentication Errors (401)

**Invalid API Key**
```json
{
  "error": {
    "message": "Invalid API key provided",
    "type": "authentication_error",
    "code": "invalid_api_key"
  }
}
```

**Missing Authorization Header**
```json
{
  "error": {
    "message": "Missing Authorization header",
    "type": "authentication_error",
    "code": "missing_authorization"
  }
}
```

**Solution:**
- Verify your API key is correct
- Ensure the Authorization header is formatted: `Bearer your-api-key`
- Check that the header is included in every request

### Invalid Request Errors (400)

**Missing Required Parameter**
```json
{
  "error": {
    "message": "Missing required parameter: messages",
    "type": "invalid_request_error",
    "code": "missing_parameter",
    "param": "messages"
  }
}
```

**Invalid Parameter Value**
```json
{
  "error": {
    "message": "Temperature must be between 0 and 2",
    "type": "invalid_request_error",
    "code": "invalid_parameter_value",
    "param": "temperature"
  }
}
```

**Model Not Found**
```json
{
  "error": {
    "message": "Model 'invalid-model' not found",
    "type": "invalid_request_error",
    "code": "model_not_found",
    "param": "model"
  }
}
```

**Context Length Exceeded**
```json
{
  "error": {
    "message": "Maximum context length exceeded: requested 150000 tokens, maximum is 8191",
    "type": "invalid_request_error",
    "code": "context_length_exceeded"
  }
}
```

**Solution:**
- Validate all parameters before sending requests
- Check parameter types and ranges
- Verify model names are correct
- Reduce message length or use a model with larger context

### Rate Limit Errors (429)

**Rate Limit Exceeded**
```json
{
  "error": {
    "message": "Rate limit exceeded. Please retry after 20 seconds",
    "type": "rate_limit_error",
    "code": "rate_limit_exceeded"
  }
}
```

**Solution:**
- Implement exponential backoff retry logic
- Reduce request frequency
- Consider upgrading your provider tier
- Use different API keys for different use cases

### Provider Errors (502)

**Provider Timeout**
```json
{
  "error": {
    "message": "Provider request timeout",
    "type": "provider_error",
    "code": "provider_timeout"
  }
}
```

**Provider API Error**
```json
{
  "error": {
    "message": "Provider API error: insufficient_quota",
    "type": "provider_error",
    "code": "provider_api_error"
  }
}
```

**Provider Not Configured**
```json
{
  "error": {
    "message": "Provider not configured for model 'gpt-4'",
    "type": "provider_error",
    "code": "provider_not_configured"
  }
}
```

**Solution:**
- Check provider API keys are configured
- Verify provider service status
- Implement fallback to alternative providers
- Contact provider for quota issues

### Server Errors (500)

**Internal Server Error**
```json
{
  "error": {
    "message": "Internal server error",
    "type": "server_error",
    "code": "internal_error"
  }
}
```

**Solution:**
- Retry the request
- Check ChoreoAI service status
- Report persistent issues to support

## Retry Strategies

### Exponential Backoff

```python
import time
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

def exponential_backoff_retry(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            # Check if error is retryable
            if hasattr(e, 'status_code'):
                if e.status_code in [429, 500, 502, 503]:
                    wait_time = 2 ** attempt  # 1, 2, 4, 8, 16 seconds
                    print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
                    time.sleep(wait_time)
                else:
                    # Don't retry client errors
                    raise
            else:
                raise

# Use it
def make_request():
    return client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )

response = exponential_backoff_retry(make_request)
```

### Simple Retry with Timeout

```python
import time

def retry_with_timeout(func, max_retries=3, timeout=30):
    start_time = time.time()

    for attempt in range(max_retries):
        if time.time() - start_time > timeout:
            raise TimeoutError("Retry timeout exceeded")

        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2)
```

### Provider Fallback

```python
def chat_with_fallback(messages):
    providers = [
        ("gpt-4", "OpenAI"),
        ("claude-3-sonnet-20240229", "Claude"),
        ("gemini-pro", "Gemini")
    ]

    last_error = None

    for model, provider_name in providers:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            print(f"Success with {provider_name}")
            return response
        except Exception as e:
            print(f"{provider_name} failed: {e}")
            last_error = e
            continue

    raise Exception(f"All providers failed. Last error: {last_error}")

# Use it
response = chat_with_fallback([
    {"role": "user", "content": "Hello"}
])
```

## Code Examples

### Basic Error Handling

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)

except Exception as e:
    print(f"Error: {e}")
```

### Detailed Error Handling

```python
import sys

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )

except ValueError as e:
    print(f"Invalid parameter: {e}")
    sys.exit(1)

except ConnectionError as e:
    print(f"Connection error: {e}")
    print("Please check your internet connection")
    sys.exit(1)

except Exception as e:
    if hasattr(e, 'status_code'):
        if e.status_code == 401:
            print("Authentication failed. Check your API key")
        elif e.status_code == 429:
            print("Rate limit exceeded. Please wait and retry")
        elif e.status_code >= 500:
            print("Server error. Please try again later")
        else:
            print(f"API error ({e.status_code}): {e}")
    else:
        print(f"Unexpected error: {e}")
    sys.exit(1)
```

### Handling Streaming Errors

```python
try:
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Write a story"}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

except Exception as e:
    print(f"\nStreaming interrupted: {e}")
    print("Partial response may be incomplete")
```

### Custom Error Classes

```python
class ChoreoAIError(Exception):
    """Base exception for ChoreoAI errors"""
    pass

class AuthenticationError(ChoreoAIError):
    """Authentication failed"""
    pass

class RateLimitError(ChoreoAIError):
    """Rate limit exceeded"""
    pass

class ProviderError(ChoreoAIError):
    """Provider-specific error"""
    pass

def make_safe_request(client, **kwargs):
    try:
        return client.chat.completions.create(**kwargs)
    except Exception as e:
        if "authentication" in str(e).lower():
            raise AuthenticationError(f"Auth failed: {e}")
        elif "rate limit" in str(e).lower():
            raise RateLimitError(f"Rate limit: {e}")
        elif "provider" in str(e).lower():
            raise ProviderError(f"Provider error: {e}")
        else:
            raise ChoreoAIError(f"Unknown error: {e}")

# Use it
try:
    response = make_safe_request(
        client,
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
except AuthenticationError:
    print("Please check your API key")
except RateLimitError:
    print("Too many requests, please slow down")
except ProviderError:
    print("Provider issue, trying fallback...")
```

### Logging Errors

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def make_request_with_logging(messages):
    try:
        logger.info("Making API request")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        logger.info("Request successful")
        return response

    except Exception as e:
        logger.error(f"Request failed: {e}", exc_info=True)
        raise

# Use it
try:
    response = make_request_with_logging([
        {"role": "user", "content": "Hello"}
    ])
except Exception:
    logger.critical("Failed to get response after retry")
```

## Best Practices

### 1. Always Handle Errors

```python
# Bad
response = client.chat.completions.create(...)

# Good
try:
    response = client.chat.completions.create(...)
except Exception as e:
    # Handle error appropriately
    pass
```

### 2. Use Specific Exception Types

```python
# Better error handling
try:
    response = client.chat.completions.create(...)
except ValueError:
    # Invalid parameters
    pass
except ConnectionError:
    # Network issues
    pass
except Exception as e:
    # Other errors
    pass
```

### 3. Implement Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def make_request():
    return client.chat.completions.create(...)
```

### 4. Log Errors for Debugging

```python
import logging

logger = logging.getLogger(__name__)

try:
    response = client.chat.completions.create(...)
except Exception as e:
    logger.exception("API request failed")
    raise
```

### 5. Provide User-Friendly Messages

```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    # Log technical details
    logger.error(f"API error: {e}")

    # Show user-friendly message
    print("Sorry, I couldn't process your request. Please try again.")
```

### 6. Set Timeouts

```python
import requests

# Set timeout for HTTP requests (if using requests library)
response = requests.post(
    url,
    json=data,
    timeout=30  # 30 second timeout
)
```

### 7. Monitor Error Rates

```python
from collections import Counter

error_counter = Counter()

def track_error(error_type):
    error_counter[error_type] += 1

    # Alert if error rate is high
    if error_counter[error_type] > 10:
        print(f"High error rate for {error_type}")

try:
    response = client.chat.completions.create(...)
except RateLimitError as e:
    track_error("rate_limit")
except ProviderError as e:
    track_error("provider")
```

## Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid API key | Wrong or missing API key | Check API key configuration |
| Model not found | Invalid model name | Verify model name spelling |
| Context length exceeded | Input too long | Reduce message length or use larger context model |
| Rate limit exceeded | Too many requests | Implement exponential backoff |
| Provider timeout | Provider slow/down | Retry or use fallback provider |
| Insufficient quota | Provider quota exhausted | Check provider billing |
| Network error | Connection issues | Check internet connection |

## Next Steps

- **[Chat Completions](chat-completions.md)** - Make API requests
- **[Streaming](streaming.md)** - Handle streaming errors
- **[Fallback Strategy](../examples/fallback-strategy.md)** - Implement fallbacks
- **[Client Documentation](../client/README.md)** - Use Python SDK error handling
