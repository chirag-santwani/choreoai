# Authentication

ChoreoAI uses API key-based authentication to secure access to the API endpoints.

## How Authentication Works

Every API request must include an API key in the `Authorization` header using the Bearer authentication scheme:

```
Authorization: Bearer your-api-key
```

## Getting API Keys

### For Development

During local development, you can use any string as your API key. The default configuration accepts all API keys.

### For Production

!!! warning
    In production, implement proper API key validation and management. Consider using:
    - A database to store and validate API keys
    - API key rotation policies
    - Key expiration mechanisms
    - Rate limiting per API key

## Adding API Keys to Requests

### cURL

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Python (requests library)

```python
import requests

headers = {
    "Authorization": "Bearer your-api-key",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
}

response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    headers=headers,
    json=data
)

print(response.json())
```

### JavaScript (fetch)

```javascript
const response = await fetch('http://localhost:8000/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-api-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'gpt-4',
    messages: [{role: 'user', content: 'Hello!'}]
  })
});

const data = await response.json();
console.log(data);
```

### Python (ChoreoAI Client)

```python
from choreoai import ChoreoAI

# Pass API key during initialization
client = ChoreoAI(api_key="your-api-key")

# Or use environment variable
# export CHOREOAI_API_KEY=your-api-key
client = ChoreoAI()  # Automatically reads from environment
```

### Python (OpenAI Client)

```python
import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Best Practices

### 1. Use Environment Variables

Never hardcode API keys in your source code. Use environment variables:

```bash
# .env file
CHOREOAI_API_KEY=your-api-key
```

```python
import os
from choreoai import ChoreoAI

api_key = os.getenv("CHOREOAI_API_KEY")
client = ChoreoAI(api_key=api_key)
```

### 2. Don't Commit API Keys

Add `.env` files to your `.gitignore`:

```gitignore
.env
.env.local
*.key
```

### 3. Rotate Keys Regularly

In production environments, implement a key rotation policy:
- Generate new keys periodically
- Revoke old or compromised keys
- Track key usage and last used date

### 4. Use Different Keys for Different Environments

```bash
# Development
CHOREOAI_API_KEY=dev-key-123

# Production
CHOREOAI_API_KEY=prod-key-456
```

### 5. Restrict Key Permissions

If implementing custom authentication, consider:
- Limiting keys to specific endpoints
- Setting rate limits per key
- Implementing IP whitelisting
- Adding key expiration

## Troubleshooting

### 401 Unauthorized

**Error:**
```json
{
  "error": {
    "message": "Invalid API key provided",
    "type": "authentication_error",
    "code": "invalid_api_key"
  }
}
```

**Solutions:**
- Verify the API key is correct
- Check that the `Authorization` header is properly formatted
- Ensure the key hasn't expired (if using expiring keys)
- Verify you're using `Bearer` scheme: `Authorization: Bearer your-key`

### Missing Authorization Header

**Error:**
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
Add the `Authorization` header to your request.

### Malformed Authorization Header

**Error:**
```json
{
  "error": {
    "message": "Malformed Authorization header",
    "type": "authentication_error",
    "code": "malformed_authorization"
  }
}
```

**Solution:**
Ensure the header follows the format: `Authorization: Bearer your-api-key`

## Provider API Keys

!!! important
    ChoreoAI requires provider API keys (OpenAI, Claude, etc.) to be configured on the server side. The ChoreoAI API key is separate from provider API keys.

**Server-side configuration** (environment variables):
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
AZURE_OPENAI_API_KEY=...
GEMINI_API_KEY=...
```

**Client-side usage:**
```python
# Only pass ChoreoAI API key, not provider keys
client = ChoreoAI(api_key="your-choreoai-api-key")
```

See [Configuration Guide](../deployment/configuration.md) for provider setup.

## Next Steps

- **[Chat Completions](chat-completions.md)** - Make your first API call
- **[Error Handling](error-handling.md)** - Handle authentication errors
- **[Configuration](../deployment/configuration.md)** - Configure provider API keys
