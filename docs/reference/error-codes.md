# Error Codes Reference

Complete reference for all error codes returned by the ChoreoAI API.

## Overview

ChoreoAI returns structured error responses with specific error codes to help you identify and resolve issues. This reference documents all error codes, their meanings, and recommended solutions.

## Error Response Format

All errors follow a consistent JSON structure:

```json
{
  "error": {
    "message": "Human-readable error description",
    "type": "error_category",
    "code": "specific_error_code",
    "param": "parameter_name"
  }
}
```

## HTTP Status Code Mapping

| HTTP Status | Error Type | Description |
|-------------|------------|-------------|
| 400 | `invalid_request_error` | Bad request or invalid parameters |
| 401 | `authentication_error` | Authentication failed |
| 403 | `permission_error` | Insufficient permissions |
| 404 | `not_found_error` | Resource not found |
| 429 | `rate_limit_error` | Rate limit exceeded |
| 500 | `server_error` | Internal server error |
| 502 | `provider_error` | Provider API error |
| 503 | `service_unavailable_error` | Service temporarily unavailable |

## Authentication Errors (401)

Errors related to API authentication and authorization.

### invalid_api_key

**Message:** "Invalid API key provided"

**Cause:** The API key is incorrect, malformed, or expired.

**Solution:**
- Verify your API key is correct
- Check for typos or extra spaces
- Ensure the key hasn't been revoked
- Generate a new API key if needed

**Example:**
```json
{
  "error": {
    "message": "Invalid API key provided",
    "type": "authentication_error",
    "code": "invalid_api_key"
  }
}
```

### missing_authorization

**Message:** "Missing Authorization header"

**Cause:** The request does not include the required Authorization header.

**Solution:**
- Add `Authorization: Bearer your-api-key` header to your request
- Verify header is properly formatted
- Check that the header is included in every request

**Example:**
```json
{
  "error": {
    "message": "Missing Authorization header",
    "type": "authentication_error",
    "code": "missing_authorization"
  }
}
```

### malformed_authorization

**Message:** "Malformed Authorization header"

**Cause:** The Authorization header format is incorrect.

**Solution:**
- Use format: `Authorization: Bearer your-api-key`
- Ensure "Bearer" is spelled correctly
- Check for missing space between "Bearer" and the key

**Example:**
```json
{
  "error": {
    "message": "Malformed Authorization header",
    "type": "authentication_error",
    "code": "malformed_authorization"
  }
}
```

### api_key_expired

**Message:** "API key has expired"

**Cause:** The API key is no longer valid due to expiration.

**Solution:**
- Generate a new API key
- Update your application configuration
- Implement key rotation policies

## Invalid Request Errors (400)

Errors caused by invalid request parameters or malformed requests.

### missing_parameter

**Message:** "Missing required parameter: {param}"

**Cause:** A required parameter is missing from the request.

**Solution:**
- Check API documentation for required parameters
- Verify all required fields are included in request
- Validate request payload before sending

**Example:**
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

### invalid_parameter_value

**Message:** "Invalid value for parameter: {param}"

**Cause:** A parameter has an invalid value.

**Solution:**
- Check valid ranges/formats for the parameter
- Verify data types match requirements
- Review API documentation for parameter constraints

**Example:**
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

### invalid_parameter_type

**Message:** "Invalid type for parameter: {param}"

**Cause:** Parameter has wrong data type.

**Solution:**
- Verify parameter types (string, number, array, etc.)
- Convert values to correct type before sending
- Check JSON serialization

**Example:**
```json
{
  "error": {
    "message": "Parameter 'max_tokens' must be an integer",
    "type": "invalid_request_error",
    "code": "invalid_parameter_type",
    "param": "max_tokens"
  }
}
```

### model_not_found

**Message:** "Model '{model}' not found"

**Cause:** The specified model does not exist or is not available.

**Solution:**
- Verify model name spelling
- Check available models using `/v1/models` endpoint
- Ensure provider is configured for the model
- Use a supported model identifier

**Example:**
```json
{
  "error": {
    "message": "Model 'gpt-5' not found",
    "type": "invalid_request_error",
    "code": "model_not_found",
    "param": "model"
  }
}
```

### context_length_exceeded

**Message:** "Maximum context length exceeded"

**Cause:** The input text exceeds the model's maximum context length.

**Solution:**
- Reduce the length of your input messages
- Use a model with larger context window
- Implement text chunking or summarization
- Remove unnecessary messages from conversation history

**Example:**
```json
{
  "error": {
    "message": "Maximum context length exceeded: requested 150000 tokens, maximum is 8191",
    "type": "invalid_request_error",
    "code": "context_length_exceeded"
  }
}
```

### invalid_messages_format

**Message:** "Invalid messages format"

**Cause:** Messages array has incorrect structure.

**Solution:**
- Use correct message format: `{"role": "user", "content": "text"}`
- Ensure messages is an array of objects
- Verify required fields (role, content) are present
- Check role values are valid (user, assistant, system)

**Example:**
```json
{
  "error": {
    "message": "Invalid messages format: expected array of objects",
    "type": "invalid_request_error",
    "code": "invalid_messages_format",
    "param": "messages"
  }
}
```

### invalid_json

**Message:** "Invalid JSON in request body"

**Cause:** Request body contains malformed JSON.

**Solution:**
- Validate JSON syntax
- Use JSON.stringify() or equivalent to ensure valid JSON
- Check for trailing commas, unquoted keys, etc.
- Use a JSON validator tool

**Example:**
```json
{
  "error": {
    "message": "Invalid JSON in request body",
    "type": "invalid_request_error",
    "code": "invalid_json"
  }
}
```

## Rate Limit Errors (429)

Errors related to exceeding rate limits.

### rate_limit_exceeded

**Message:** "Rate limit exceeded. Please retry after {seconds} seconds"

**Cause:** Too many requests in a short time period.

**Solution:**
- Implement exponential backoff retry logic
- Reduce request frequency
- Use batch processing where possible
- Consider upgrading your plan
- Distribute load across multiple API keys

**Example:**
```json
{
  "error": {
    "message": "Rate limit exceeded. Please retry after 20 seconds",
    "type": "rate_limit_error",
    "code": "rate_limit_exceeded"
  }
}
```

### quota_exceeded

**Message:** "API quota exceeded"

**Cause:** Monthly or daily usage quota has been reached.

**Solution:**
- Check your usage dashboard
- Upgrade your plan for higher quota
- Wait for quota reset
- Optimize API usage to reduce calls

**Example:**
```json
{
  "error": {
    "message": "Monthly API quota exceeded",
    "type": "rate_limit_error",
    "code": "quota_exceeded"
  }
}
```

## Provider Errors (502)

Errors from AI provider services.

### provider_timeout

**Message:** "Provider request timeout"

**Cause:** Provider API did not respond within timeout period.

**Solution:**
- Retry the request
- Implement timeout handling
- Use fallback providers
- Check provider service status
- Increase timeout settings if appropriate

**Example:**
```json
{
  "error": {
    "message": "Provider request timeout after 30 seconds",
    "type": "provider_error",
    "code": "provider_timeout"
  }
}
```

### provider_api_error

**Message:** "Provider API error: {details}"

**Cause:** The AI provider returned an error.

**Solution:**
- Check provider API status
- Verify provider API key is valid
- Review provider-specific error details
- Check provider billing and quota
- Contact provider support if issue persists

**Example:**
```json
{
  "error": {
    "message": "Provider API error: insufficient_quota",
    "type": "provider_error",
    "code": "provider_api_error"
  }
}
```

### provider_not_configured

**Message:** "Provider not configured for model '{model}'"

**Cause:** The required provider API key is not configured.

**Solution:**
- Configure provider API key in environment variables
- Verify provider credentials are correct
- Check `.env` file configuration
- Restart server after adding credentials
- Use a model from a configured provider

**Example:**
```json
{
  "error": {
    "message": "Provider not configured for model 'gpt-4'",
    "type": "provider_error",
    "code": "provider_not_configured"
  }
}
```

### provider_service_unavailable

**Message:** "Provider service temporarily unavailable"

**Cause:** Provider API is down or experiencing issues.

**Solution:**
- Check provider status page
- Retry after a delay
- Use fallback provider
- Monitor provider status updates
- Implement circuit breaker pattern

**Example:**
```json
{
  "error": {
    "message": "OpenAI service temporarily unavailable",
    "type": "provider_error",
    "code": "provider_service_unavailable"
  }
}
```

## Server Errors (500)

Internal server errors.

### internal_error

**Message:** "Internal server error"

**Cause:** An unexpected error occurred on the server.

**Solution:**
- Retry the request
- Check server logs for details
- Report persistent issues
- Verify request format is correct
- Check server health status

**Example:**
```json
{
  "error": {
    "message": "Internal server error",
    "type": "server_error",
    "code": "internal_error"
  }
}
```

### configuration_error

**Message:** "Server configuration error"

**Cause:** Server is misconfigured.

**Solution:**
- Verify environment variables
- Check configuration files
- Review server logs
- Restart server with correct configuration
- Contact system administrator

**Example:**
```json
{
  "error": {
    "message": "Server configuration error: missing required settings",
    "type": "server_error",
    "code": "configuration_error"
  }
}
```

## Not Found Errors (404)

Resource or endpoint not found.

### endpoint_not_found

**Message:** "Endpoint not found"

**Cause:** The requested endpoint does not exist.

**Solution:**
- Verify endpoint URL is correct
- Check API documentation for valid endpoints
- Ensure correct API version in URL
- Remove trailing slashes if present

**Example:**
```json
{
  "error": {
    "message": "Endpoint '/v1/invalid' not found",
    "type": "not_found_error",
    "code": "endpoint_not_found"
  }
}
```

### resource_not_found

**Message:** "Resource not found"

**Cause:** The requested resource does not exist.

**Solution:**
- Verify resource ID is correct
- Check if resource was deleted
- Use list endpoint to see available resources
- Ensure you have access to the resource

**Example:**
```json
{
  "error": {
    "message": "Model 'custom-model-123' not found",
    "type": "not_found_error",
    "code": "resource_not_found"
  }
}
```

## Service Unavailable Errors (503)

Service temporarily unavailable.

### service_overloaded

**Message:** "Service temporarily overloaded"

**Cause:** Server is under heavy load.

**Solution:**
- Retry after a delay
- Implement exponential backoff
- Use off-peak hours if possible
- Consider scaling infrastructure
- Monitor service status

**Example:**
```json
{
  "error": {
    "message": "Service temporarily overloaded. Please retry in 30 seconds",
    "type": "service_unavailable_error",
    "code": "service_overloaded"
  }
}
```

### maintenance_mode

**Message:** "Service under maintenance"

**Cause:** Server is in maintenance mode.

**Solution:**
- Wait for maintenance to complete
- Check status page for updates
- Subscribe to maintenance notifications
- Use backup instance if available

**Example:**
```json
{
  "error": {
    "message": "Service under maintenance. Expected completion: 2024-01-15 10:00 UTC",
    "type": "service_unavailable_error",
    "code": "maintenance_mode"
  }
}
```

## Error Code Summary Table

| Code | HTTP Status | Type | Retry? | Description |
|------|-------------|------|--------|-------------|
| `invalid_api_key` | 401 | authentication_error | No | Invalid or expired API key |
| `missing_authorization` | 401 | authentication_error | No | Missing Authorization header |
| `malformed_authorization` | 401 | authentication_error | No | Malformed Authorization header |
| `missing_parameter` | 400 | invalid_request_error | No | Required parameter missing |
| `invalid_parameter_value` | 400 | invalid_request_error | No | Invalid parameter value |
| `invalid_parameter_type` | 400 | invalid_request_error | No | Wrong parameter type |
| `model_not_found` | 400 | invalid_request_error | No | Model doesn't exist |
| `context_length_exceeded` | 400 | invalid_request_error | No | Input too long |
| `invalid_messages_format` | 400 | invalid_request_error | No | Messages array malformed |
| `invalid_json` | 400 | invalid_request_error | No | Malformed JSON request |
| `rate_limit_exceeded` | 429 | rate_limit_error | Yes | Too many requests |
| `quota_exceeded` | 429 | rate_limit_error | No | Usage quota exceeded |
| `provider_timeout` | 502 | provider_error | Yes | Provider timeout |
| `provider_api_error` | 502 | provider_error | Maybe | Provider returned error |
| `provider_not_configured` | 502 | provider_error | No | Provider not set up |
| `provider_service_unavailable` | 502 | provider_error | Yes | Provider is down |
| `internal_error` | 500 | server_error | Yes | Server error |
| `configuration_error` | 500 | server_error | No | Server misconfigured |
| `endpoint_not_found` | 404 | not_found_error | No | Invalid endpoint |
| `resource_not_found` | 404 | not_found_error | No | Resource doesn't exist |
| `service_overloaded` | 503 | service_unavailable_error | Yes | Server overloaded |
| `maintenance_mode` | 503 | service_unavailable_error | Yes | Under maintenance |

## Handling Errors in Code

### Python

```python
from choreoai import ChoreoAI
import time

client = ChoreoAI(api_key="your-api-key")

def handle_error(error_code, error_message):
    """Handle specific error codes"""
    if error_code == "rate_limit_exceeded":
        print("Rate limit hit, waiting...")
        time.sleep(20)
        return True  # Retry
    elif error_code == "provider_timeout":
        print("Provider timeout, retrying...")
        time.sleep(5)
        return True  # Retry
    elif error_code == "invalid_api_key":
        print("Invalid API key, cannot retry")
        return False  # Don't retry
    elif error_code in ["model_not_found", "missing_parameter"]:
        print(f"Client error: {error_message}")
        return False  # Don't retry
    else:
        print(f"Unknown error: {error_message}")
        return False

# Use the error handler
max_retries = 3
for attempt in range(max_retries):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}]
        )
        break
    except Exception as e:
        if hasattr(e, 'error') and hasattr(e.error, 'code'):
            should_retry = handle_error(e.error.code, e.error.message)
            if not should_retry or attempt == max_retries - 1:
                raise
        else:
            raise
```

### JavaScript

```javascript
async function handleChoreoAIError(error) {
  const retryableErrors = [
    'rate_limit_exceeded',
    'provider_timeout',
    'service_overloaded',
    'internal_error'
  ];

  if (error.code && retryableErrors.includes(error.code)) {
    // Exponential backoff
    const delay = Math.pow(2, attempt) * 1000;
    await new Promise(resolve => setTimeout(resolve, delay));
    return true; // Retry
  }

  return false; // Don't retry
}

// Usage
for (let attempt = 0; attempt < 3; attempt++) {
  try {
    const response = await choreoai.chat.completions.create({
      model: 'gpt-4',
      messages: [{role: 'user', content: 'Hello'}]
    });
    break;
  } catch (error) {
    const shouldRetry = await handleChoreoAIError(error);
    if (!shouldRetry || attempt === 2) {
      throw error;
    }
  }
}
```

## Best Practices

### 1. Implement Retry Logic for Transient Errors

```python
RETRYABLE_CODES = [
    "rate_limit_exceeded",
    "provider_timeout",
    "service_overloaded",
    "internal_error"
]

def should_retry(error_code):
    return error_code in RETRYABLE_CODES
```

### 2. Use Exponential Backoff

```python
def exponential_backoff(attempt):
    return min(60, 2 ** attempt)  # Max 60 seconds
```

### 3. Log Error Details

```python
import logging

logger = logging.getLogger(__name__)

try:
    response = client.chat.completions.create(...)
except Exception as e:
    logger.error(f"API Error: {e.error.code} - {e.error.message}")
    logger.error(f"Request params: {e.request}")
```

### 4. Implement Fallback Strategies

```python
def chat_with_fallback(messages):
    providers = [
        ("gpt-4", "OpenAI"),
        ("claude-3-sonnet-20240229", "Claude"),
        ("gemini-pro", "Gemini")
    ]

    for model, name in providers:
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages
            )
        except Exception as e:
            logger.warning(f"{name} failed: {e.error.code}")
            continue

    raise Exception("All providers failed")
```

### 5. Monitor Error Rates

```python
from collections import Counter

error_counter = Counter()

def track_error(error_code):
    error_counter[error_code] += 1

    # Alert on high error rates
    if error_counter[error_code] > 10:
        alert_team(f"High error rate for {error_code}")
```

## Related Documentation

- **[Error Handling Guide](../api/error-handling.md)** - Comprehensive error handling
- **[Authentication](../api/authentication.md)** - Authentication setup
- **[Environment Variables](environment-vars.md)** - Configuration reference
- **[FAQ](faq.md)** - Frequently asked questions
