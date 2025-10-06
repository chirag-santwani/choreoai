# Environment Variables Reference

Complete reference for all environment variables used in ChoreoAI.

## Overview

ChoreoAI uses environment variables to configure the API server, provider integrations, and operational settings. This reference documents all available environment variables, their purpose, and valid values.

## Configuration File

Environment variables can be set in a `.env` file in your project root:

```bash
# .env
PORT=8000
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## Server Configuration

Configure the FastAPI server and runtime environment.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PORT` | integer | `8000` | Port number for the API server |
| `HOST` | string | `0.0.0.0` | Host address to bind the server |
| `LOG_LEVEL` | string | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `ENVIRONMENT` | string | `development` | Runtime environment (development, staging, production) |

### Examples

```bash
# Development
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=DEBUG
ENVIRONMENT=development

# Production
PORT=80
HOST=0.0.0.0
LOG_LEVEL=WARNING
ENVIRONMENT=production
```

## CORS Configuration

Configure Cross-Origin Resource Sharing (CORS) settings.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ALLOWED_ORIGINS` | string | `*` | Comma-separated list of allowed origins for CORS |

### Examples

```bash
# Allow all origins (development only)
ALLOWED_ORIGINS=*

# Allow specific origins (production)
ALLOWED_ORIGINS=https://app.example.com,https://admin.example.com
```

## Provider API Keys

Configure API keys for AI provider integrations.

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `OPENAI_API_KEY` | string | Optional | OpenAI API key (starts with `sk-`) |
| `ANTHROPIC_API_KEY` | string | Optional | Anthropic/Claude API key (starts with `sk-ant-`) |
| `AZURE_OPENAI_ENDPOINT` | string | Optional | Azure OpenAI endpoint URL |
| `AZURE_OPENAI_API_KEY` | string | Optional | Azure OpenAI API key |
| `GEMINI_API_KEY` | string | Optional | Google Gemini API key |
| `GROK_API_KEY` | string | Optional | xAI Grok API key |

### Provider-Specific Details

#### OpenAI

```bash
OPENAI_API_KEY=sk-proj-abcdefghijklmnopqrstuvwxyz1234567890
```

- Obtain from: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Format: Starts with `sk-` or `sk-proj-`
- Models enabled: GPT-4, GPT-3.5-turbo, embeddings

#### Anthropic (Claude)

```bash
ANTHROPIC_API_KEY=sk-ant-api03-abcdefghijklmnopqrstuvwxyz1234567890
```

- Obtain from: [console.anthropic.com](https://console.anthropic.com)
- Format: Starts with `sk-ant-`
- Models enabled: Claude 3 Opus, Sonnet, Haiku, Claude 2

#### Azure OpenAI

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=abcdefghijklmnopqrstuvwxyz1234567890
```

- Obtain from: [portal.azure.com](https://portal.azure.com)
- Requires: Azure subscription and OpenAI resource
- Models enabled: GPT-4, GPT-3.5 (deployment-specific)

#### Google Gemini

```bash
GEMINI_API_KEY=AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567
```

- Obtain from: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- Format: Starts with `AIzaSy`
- Models enabled: Gemini Pro, Gemini Pro Vision

#### xAI Grok

```bash
GROK_API_KEY=xai-abcdefghijklmnopqrstuvwxyz1234567890
```

- Obtain from: [x.ai](https://x.ai)
- Format: Starts with `xai-`
- Models enabled: Grok models

## AWS Configuration (for Bedrock)

Configure AWS credentials for Amazon Bedrock integration.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `AWS_REGION` | string | `us-east-1` | AWS region for Bedrock service |
| `AWS_ACCESS_KEY_ID` | string | Optional | AWS access key ID |
| `AWS_SECRET_ACCESS_KEY` | string | Optional | AWS secret access key |

### Examples

```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### Supported Regions

- `us-east-1` - US East (N. Virginia)
- `us-west-2` - US West (Oregon)
- `eu-west-1` - Europe (Ireland)
- `ap-southeast-1` - Asia Pacific (Singapore)
- `ap-northeast-1` - Asia Pacific (Tokyo)

## Client Configuration

Environment variables for the Python client library.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CHOREOAI_API_KEY` | string | Required | API key for authenticating with ChoreoAI |
| `CHOREOAI_BASE_URL` | string | `http://localhost:8000` | Base URL of the ChoreoAI API |

### Examples

```bash
# Local development
CHOREOAI_API_KEY=dev-key-123
CHOREOAI_BASE_URL=http://localhost:8000

# Production
CHOREOAI_API_KEY=prod-key-456
CHOREOAI_BASE_URL=https://api.choreoai.com
```

## Usage in Code

### Python (Server)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = 8000
    OPENAI_API_KEY: str = None

    class Config:
        env_file = ".env"

settings = Settings()
```

### Python (Client)

```python
import os
from choreoai import ChoreoAI

# Automatic from environment
client = ChoreoAI()

# Or explicit
client = ChoreoAI(
    api_key=os.getenv("CHOREOAI_API_KEY"),
    base_url=os.getenv("CHOREOAI_BASE_URL")
)
```

### Docker

```dockerfile
# Dockerfile
ENV PORT=8000
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    environment:
      - PORT=8000
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
```

### Kubernetes

```yaml
# deployment.yaml
apiVersion: v1
kind: Secret
metadata:
  name: choreoai-secrets
type: Opaque
stringData:
  OPENAI_API_KEY: sk-...
  ANTHROPIC_API_KEY: sk-ant-...
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: api
        envFrom:
        - secretRef:
            name: choreoai-secrets
```

## Security Best Practices

### 1. Never Commit API Keys

Add `.env` to `.gitignore`:

```gitignore
# .gitignore
.env
.env.*
!.env.example
*.key
```

### 2. Use Different Keys per Environment

```bash
# .env.development
OPENAI_API_KEY=sk-dev-...

# .env.production
OPENAI_API_KEY=sk-prod-...
```

### 3. Rotate Keys Regularly

- Set key expiration dates
- Rotate keys every 90 days
- Revoke compromised keys immediately

### 4. Use Secret Management

**AWS Secrets Manager:**
```bash
aws secretsmanager get-secret-value \
  --secret-id choreoai/openai-key \
  --query SecretString \
  --output text
```

**HashiCorp Vault:**
```bash
vault kv get -field=api_key secret/choreoai/openai
```

**Kubernetes Secrets:**
```bash
kubectl create secret generic choreoai-keys \
  --from-literal=OPENAI_API_KEY=sk-...
```

### 5. Limit Key Permissions

- Use read-only keys when possible
- Restrict keys to specific IP ranges
- Set usage quotas and rate limits

## Environment-Specific Configuration

### Development

```bash
# .env.development
PORT=8000
HOST=localhost
LOG_LEVEL=DEBUG
ENVIRONMENT=development
ALLOWED_ORIGINS=*
OPENAI_API_KEY=sk-dev-...
```

### Staging

```bash
# .env.staging
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=INFO
ENVIRONMENT=staging
ALLOWED_ORIGINS=https://staging.example.com
OPENAI_API_KEY=sk-staging-...
```

### Production

```bash
# .env.production
PORT=80
HOST=0.0.0.0
LOG_LEVEL=WARNING
ENVIRONMENT=production
ALLOWED_ORIGINS=https://app.example.com
OPENAI_API_KEY=sk-prod-...
```

## Validation

### Required Variables

The following variables must be set for the API to function:

- At least one provider API key (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)

### Optional Variables

All other variables have sensible defaults and are optional.

### Validation at Startup

ChoreoAI validates configuration on startup:

```python
# Startup validation
if not any([
    settings.OPENAI_API_KEY,
    settings.ANTHROPIC_API_KEY,
    settings.AZURE_OPENAI_API_KEY,
    settings.GEMINI_API_KEY
]):
    raise ValueError("At least one provider API key must be configured")
```

## Troubleshooting

### Issue: Environment Variables Not Loading

**Solution:**
1. Check `.env` file location (must be in project root)
2. Verify file name is exactly `.env`
3. Ensure no syntax errors in `.env` file
4. Restart the application after changes

### Issue: Invalid API Key Format

**Solution:**
1. Verify key format matches provider requirements
2. Check for extra spaces or newlines
3. Ensure key is not expired
4. Test key directly with provider API

### Issue: Provider Not Available

**Solution:**
1. Verify provider API key is set
2. Check provider service status
3. Ensure key has required permissions
4. Verify billing is active on provider account

## Example Configuration Files

### Complete .env Example

```bash
# Server Configuration
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=INFO
ENVIRONMENT=production

# CORS
ALLOWED_ORIGINS=https://app.example.com,https://admin.example.com

# Provider API Keys
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-api03-...
AZURE_OPENAI_ENDPOINT=https://my-resource.openai.azure.com
AZURE_OPENAI_API_KEY=...
GEMINI_API_KEY=AIzaSy...
GROK_API_KEY=xai-...

# AWS (for Bedrock)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
```

### Minimal .env Example

```bash
# Minimum required configuration
PORT=8000
OPENAI_API_KEY=sk-...
```

### .env.example Template

```bash
# Server Configuration
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=INFO
ENVIRONMENT=development

# CORS
ALLOWED_ORIGINS=*

# Provider API Keys (at least one required)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
GEMINI_API_KEY=
GROK_API_KEY=

# AWS Configuration (optional, for Bedrock)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

## Related Documentation

- **[Authentication](../api/authentication.md)** - API authentication
- **[Configuration](../deployment/configuration.md)** - Deployment configuration
- **[Providers](../providers/README.md)** - Provider setup guides
- **[Error Codes](error-codes.md)** - Error code reference
