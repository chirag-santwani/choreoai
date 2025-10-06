# Configuration Reference

Complete configuration reference for ChoreoAI deployment across all environments and platforms.

## Table of Contents

- [Overview](#overview)
- [Environment Variables](#environment-variables)
- [Provider Configuration](#provider-configuration)
- [Server Configuration](#server-configuration)
- [Security Configuration](#security-configuration)
- [Logging Configuration](#logging-configuration)
- [Performance Configuration](#performance-configuration)
- [Feature Flags](#feature-flags)
- [Configuration by Deployment Method](#configuration-by-deployment-method)
- [Configuration Validation](#configuration-validation)
- [Environment-specific Configurations](#environment-specific-configurations)
- [Configuration Best Practices](#configuration-best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

ChoreoAI uses environment variables for all configuration. This approach:

- Works across all deployment methods (Docker, Kubernetes, Helm)
- Follows the 12-factor app methodology
- Simplifies secret management
- Enables environment-specific configurations

### Configuration Priority

Configuration is loaded in the following order (later overrides earlier):

1. Default values (in code)
2. Environment variables
3. `.env` file (development only)
4. Command-line arguments (if applicable)

## Environment Variables

### Complete Reference Table

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| **Server Configuration** |
| `PORT` | integer | No | `8000` | Server port number |
| `HOST` | string | No | `0.0.0.0` | Server host address |
| `ENVIRONMENT` | string | No | `development` | Environment name (development, staging, production) |
| `LOG_LEVEL` | string | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `WORKERS` | integer | No | `1` | Number of worker processes |
| `ALLOWED_ORIGINS` | string | No | `*` | CORS allowed origins (comma-separated) |
| **Provider API Keys** |
| `OPENAI_API_KEY` | string | No* | - | OpenAI API key |
| `ANTHROPIC_API_KEY` | string | No* | - | Anthropic (Claude) API key |
| `GEMINI_API_KEY` | string | No* | - | Google Gemini API key |
| `GROK_API_KEY` | string | No* | - | xAI Grok API key |
| `AZURE_OPENAI_API_KEY` | string | No* | - | Azure OpenAI API key |
| `AZURE_OPENAI_ENDPOINT` | string | No | - | Azure OpenAI endpoint URL |
| `AZURE_OPENAI_API_VERSION` | string | No | `2024-02-15-preview` | Azure OpenAI API version |
| **AWS Configuration (for Bedrock)** |
| `AWS_REGION` | string | No | `us-east-1` | AWS region |
| `AWS_ACCESS_KEY_ID` | string | No | - | AWS access key ID |
| `AWS_SECRET_ACCESS_KEY` | string | No | - | AWS secret access key |
| `AWS_SESSION_TOKEN` | string | No | - | AWS session token (for temporary credentials) |
| **Rate Limiting** |
| `RATE_LIMIT_ENABLED` | boolean | No | `true` | Enable rate limiting |
| `RATE_LIMIT_REQUESTS` | integer | No | `100` | Max requests per window |
| `RATE_LIMIT_WINDOW` | integer | No | `60` | Rate limit window in seconds |
| **Caching** |
| `CACHE_ENABLED` | boolean | No | `false` | Enable response caching |
| `CACHE_TTL` | integer | No | `300` | Cache TTL in seconds |
| `REDIS_URL` | string | No | - | Redis connection URL for caching |
| **Timeouts** |
| `REQUEST_TIMEOUT` | integer | No | `300` | Request timeout in seconds |
| `PROVIDER_TIMEOUT` | integer | No | `180` | Provider API timeout in seconds |
| **Retry Configuration** |
| `RETRY_ENABLED` | boolean | No | `true` | Enable automatic retries |
| `RETRY_MAX_ATTEMPTS` | integer | No | `3` | Maximum retry attempts |
| `RETRY_BACKOFF_FACTOR` | float | No | `2.0` | Exponential backoff factor |
| **Authentication** |
| `AUTH_ENABLED` | boolean | No | `false` | Enable API authentication |
| `API_KEYS` | string | No | - | Comma-separated list of valid API keys |
| `JWT_SECRET` | string | No | - | JWT secret for token validation |
| **Monitoring** |
| `METRICS_ENABLED` | boolean | No | `true` | Enable Prometheus metrics |
| `METRICS_PORT` | integer | No | `8000` | Metrics endpoint port |
| `TRACING_ENABLED` | boolean | No | `false` | Enable distributed tracing |
| `JAEGER_ENDPOINT` | string | No | - | Jaeger collector endpoint |

*At least one provider API key is required

## Provider Configuration

### OpenAI

```bash
# Required
OPENAI_API_KEY=sk-proj-your-openai-api-key

# Optional
OPENAI_ORG_ID=org-your-organization-id
OPENAI_BASE_URL=https://api.openai.com/v1  # Custom base URL
```

**Supported Models:**
- GPT-4 family: `gpt-4`, `gpt-4-turbo`, `gpt-4-turbo-preview`
- GPT-3.5 family: `gpt-3.5-turbo`, `gpt-3.5-turbo-16k`
- Embeddings: `text-embedding-ada-002`, `text-embedding-3-small`, `text-embedding-3-large`

### Anthropic (Claude)

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key

# Optional
ANTHROPIC_BASE_URL=https://api.anthropic.com  # Custom base URL
ANTHROPIC_API_VERSION=2023-06-01              # API version
```

**Supported Models:**
- Claude 3: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- Claude 2: `claude-2.1`, `claude-2.0`
- Claude Instant: `claude-instant-1.2`

### Google Gemini

```bash
# Required
GEMINI_API_KEY=your-gemini-api-key

# Optional
GEMINI_BASE_URL=https://generativelanguage.googleapis.com
```

**Supported Models:**
- Gemini Pro: `gemini-pro`, `gemini-pro-vision`
- Gemini Ultra: `gemini-ultra`

### xAI Grok

```bash
# Required
GROK_API_KEY=your-grok-api-key

# Optional
GROK_BASE_URL=https://api.x.ai/v1
```

**Supported Models:**
- `grok-1`
- `grok-beta`

### Azure OpenAI

```bash
# Required
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# Optional
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name  # Default deployment
```

**Configuration Notes:**
- Azure uses deployment names instead of model names
- Endpoint format: `https://{resource-name}.openai.azure.com`
- Supports same models as OpenAI (with appropriate deployments)

### AWS Bedrock

```bash
# Required (one of the following methods)

# Method 1: IAM credentials
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1

# Method 2: IAM role (for EKS/EC2)
AWS_REGION=us-east-1
# No credentials needed - uses instance/pod role

# Method 3: Session credentials
AWS_ACCESS_KEY_ID=ASIA...
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_SESSION_TOKEN=your-session-token
AWS_REGION=us-east-1
```

**Supported Models:**
- Claude: `anthropic.claude-v2`, `anthropic.claude-instant-v1`
- Titan: `amazon.titan-text-express-v1`
- Jurassic: `ai21.j2-ultra-v1`

## Server Configuration

### Basic Server Settings

```bash
# Server host and port
HOST=0.0.0.0          # Bind to all interfaces
PORT=8000             # Server port

# Environment
ENVIRONMENT=production  # development, staging, production

# Workers (for production)
WORKERS=4             # Number of uvicorn workers
```

### CORS Configuration

```bash
# Allow all origins (development only)
ALLOWED_ORIGINS=*

# Allow specific origins (production)
ALLOWED_ORIGINS=https://app.example.com,https://dashboard.example.com

# Multiple origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://example.com
```

### Worker Configuration

```bash
# Single worker (development)
WORKERS=1

# Multiple workers (production)
WORKERS=4  # Recommended: 2-4 × CPU cores

# Auto-detect CPU cores
WORKERS=auto
```

## Security Configuration

### Authentication

```bash
# Enable authentication
AUTH_ENABLED=true

# API key authentication
API_KEYS=key1,key2,key3

# JWT authentication
JWT_SECRET=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600  # Token expiration in seconds
```

### API Key Usage

```bash
# Request with API key
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4", "messages": [...]}'
```

### TLS/SSL Configuration

```bash
# Enable HTTPS (behind proxy)
FORCE_SSL=true
SSL_REDIRECT=true

# Custom SSL certificates (direct HTTPS)
SSL_CERT_FILE=/path/to/cert.pem
SSL_KEY_FILE=/path/to/key.pem
```

### Rate Limiting

```bash
# Enable rate limiting
RATE_LIMIT_ENABLED=true

# Rate limit configuration
RATE_LIMIT_REQUESTS=100      # Max requests
RATE_LIMIT_WINDOW=60         # Time window in seconds
RATE_LIMIT_BY=ip            # Rate limit by: ip, api_key, user

# Custom rate limits per endpoint
RATE_LIMIT_CHAT=50          # Requests per minute for /v1/chat/completions
RATE_LIMIT_EMBEDDINGS=200   # Requests per minute for /v1/embeddings
```

## Logging Configuration

### Log Levels

```bash
# Development
LOG_LEVEL=DEBUG    # Most verbose

# Staging
LOG_LEVEL=INFO     # Standard logging

# Production
LOG_LEVEL=WARNING  # Warnings and errors only
```

**Available Levels:**
- `DEBUG`: Detailed debug information
- `INFO`: General informational messages
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors only

### Log Format

```bash
# JSON format (production)
LOG_FORMAT=json

# Text format (development)
LOG_FORMAT=text

# Custom format
LOG_FORMAT=custom
LOG_FORMAT_STRING="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Log Output

```bash
# Console output (default)
LOG_OUTPUT=console

# File output
LOG_OUTPUT=file
LOG_FILE_PATH=/var/log/choreoai/app.log

# Both console and file
LOG_OUTPUT=both

# Structured logging
LOG_STRUCTURED=true
```

### Log Rotation

```bash
# Enable log rotation
LOG_ROTATION_ENABLED=true

# Rotation settings
LOG_ROTATION_MAX_BYTES=10485760    # 10MB
LOG_ROTATION_BACKUP_COUNT=5        # Keep 5 backup files
LOG_ROTATION_WHEN=midnight         # Rotate at midnight
```

## Performance Configuration

### Timeouts

```bash
# Overall request timeout
REQUEST_TIMEOUT=300         # 5 minutes

# Provider API timeout
PROVIDER_TIMEOUT=180        # 3 minutes

# Connection timeout
CONNECTION_TIMEOUT=30       # 30 seconds

# Read timeout
READ_TIMEOUT=180           # 3 minutes
```

### Connection Pooling

```bash
# HTTP connection pool
CONNECTION_POOL_SIZE=100
CONNECTION_POOL_MAXSIZE=200
CONNECTION_POOL_KEEPALIVE=300  # seconds
```

### Retry Configuration

```bash
# Enable retries
RETRY_ENABLED=true

# Retry settings
RETRY_MAX_ATTEMPTS=3
RETRY_BACKOFF_FACTOR=2.0
RETRY_BACKOFF_MAX=60        # Max backoff in seconds

# Retry on specific status codes
RETRY_STATUS_CODES=429,500,502,503,504
```

### Caching

```bash
# Enable caching
CACHE_ENABLED=true

# Cache backend
CACHE_BACKEND=redis         # redis, memory, or memcached

# Redis configuration
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your-password
REDIS_DB=0

# Cache TTL
CACHE_TTL=300              # 5 minutes
CACHE_MAX_SIZE=1000        # Max cached items (memory backend)
```

### Request Size Limits

```bash
# Max request body size
MAX_REQUEST_SIZE=10485760   # 10MB

# Max tokens per request
MAX_TOKENS_PER_REQUEST=4096

# Max concurrent requests
MAX_CONCURRENT_REQUESTS=100
```

## Feature Flags

### Streaming

```bash
# Enable streaming responses
STREAMING_ENABLED=true

# Stream buffer size
STREAM_BUFFER_SIZE=8192
```

### Embeddings

```bash
# Enable embeddings endpoint
EMBEDDINGS_ENABLED=true

# Max batch size for embeddings
EMBEDDINGS_MAX_BATCH_SIZE=100
```

### Function Calling

```bash
# Enable function calling
FUNCTION_CALLING_ENABLED=true

# Max functions per request
MAX_FUNCTIONS_PER_REQUEST=10
```

### Provider Fallback

```bash
# Enable automatic failover
FALLBACK_ENABLED=true

# Fallback chain (comma-separated)
FALLBACK_CHAIN=openai,anthropic,gemini

# Fallback on errors
FALLBACK_ON_ERROR=true
FALLBACK_ON_TIMEOUT=true
```

## Configuration by Deployment Method

### Docker

**.env file:**
```bash
# .env
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=INFO
ENVIRONMENT=production

OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
```

**Docker command:**
```bash
docker run -d \
  --name choreoai \
  -p 8000:8000 \
  --env-file .env \
  choreoai/choreoai:latest
```

### Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  choreoai:
    image: choreoai/choreoai:latest
    env_file:
      - .env
    environment:
      - PORT=8000
      - HOST=0.0.0.0
      - LOG_LEVEL=INFO
    ports:
      - "8000:8000"
```

### Kubernetes

**ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: choreoai-config
data:
  PORT: "8000"
  HOST: "0.0.0.0"
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
```

**Secret:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: choreoai-secrets
type: Opaque
stringData:
  OPENAI_API_KEY: sk-your-key
  ANTHROPIC_API_KEY: sk-ant-your-key
```

**Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: choreoai
spec:
  template:
    spec:
      containers:
      - name: choreoai
        envFrom:
        - configMapRef:
            name: choreoai-config
        - secretRef:
            name: choreoai-secrets
```

### Helm

**values.yaml:**
```yaml
env:
  PORT: "8000"
  HOST: "0.0.0.0"
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"

secrets:
  openai_api_key: sk-your-key
  anthropic_api_key: sk-ant-your-key
```

**Install command:**
```bash
helm install choreoai choreoai/choreoai \
  --values values-production.yaml
```

## Configuration Validation

### Required Checks

```python
# Pseudo-code for validation
def validate_config():
    # At least one provider API key required
    if not any([
        OPENAI_API_KEY,
        ANTHROPIC_API_KEY,
        GEMINI_API_KEY,
        AZURE_OPENAI_API_KEY,
        AWS_ACCESS_KEY_ID
    ]):
        raise ValueError("At least one provider API key is required")

    # Port must be valid
    if not 1 <= PORT <= 65535:
        raise ValueError("PORT must be between 1 and 65535")

    # Log level must be valid
    if LOG_LEVEL not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise ValueError("Invalid LOG_LEVEL")
```

### Validation Endpoint

```bash
# Check configuration
curl http://localhost:8000/v1/config/validate

# Response
{
  "valid": true,
  "providers": ["openai", "anthropic"],
  "warnings": []
}
```

## Environment-specific Configurations

### Development

```bash
# .env.development
ENVIRONMENT=development
LOG_LEVEL=DEBUG
LOG_FORMAT=text

# Allow all CORS
ALLOWED_ORIGINS=*

# Disable authentication
AUTH_ENABLED=false

# Enable detailed logging
DEBUG=true

# Disable rate limiting
RATE_LIMIT_ENABLED=false

# Provider keys
OPENAI_API_KEY=sk-dev-key
ANTHROPIC_API_KEY=sk-ant-dev-key
```

### Staging

```bash
# .env.staging
ENVIRONMENT=staging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Specific origins
ALLOWED_ORIGINS=https://staging.example.com

# Enable authentication
AUTH_ENABLED=true
API_KEYS=staging-key-1,staging-key-2

# Moderate rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=200

# Provider keys
OPENAI_API_KEY=sk-staging-key
ANTHROPIC_API_KEY=sk-ant-staging-key
```

### Production

```bash
# .env.production
ENVIRONMENT=production
LOG_LEVEL=WARNING
LOG_FORMAT=json

# Specific origins
ALLOWED_ORIGINS=https://app.example.com,https://dashboard.example.com

# Enable authentication
AUTH_ENABLED=true

# Strict rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Enable caching
CACHE_ENABLED=true
REDIS_URL=redis://redis:6379/0

# Enable monitoring
METRICS_ENABLED=true
TRACING_ENABLED=true

# Timeouts
REQUEST_TIMEOUT=300
PROVIDER_TIMEOUT=180

# Workers
WORKERS=4

# Provider keys (from secrets manager)
OPENAI_API_KEY=${OPENAI_API_KEY}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
```

## Configuration Best Practices

### 1. Use Environment-specific Files

```bash
.env.development
.env.staging
.env.production
.env.local  # Local overrides (git-ignored)
```

### 2. Never Commit Secrets

```gitignore
# .gitignore
.env
.env.local
.env.*.local
secrets/
*.key
*.pem
```

### 3. Use Secret Management

```bash
# AWS Secrets Manager
aws secretsmanager get-secret-value \
  --secret-id choreoai/production/openai-key \
  --query SecretString \
  --output text

# HashiCorp Vault
vault kv get secret/choreoai/production/openai-key
```

### 4. Validate on Startup

```python
# Validate configuration on application startup
def startup_event():
    validate_config()
    log_config_summary()
    check_provider_connectivity()
```

### 5. Document All Variables

```bash
# .env.example - Template file
# Server Configuration
PORT=8000                    # Server port
HOST=0.0.0.0                # Server host

# Provider API Keys (required - at least one)
OPENAI_API_KEY=             # OpenAI API key
ANTHROPIC_API_KEY=          # Anthropic API key
```

### 6. Use Type Conversion

```python
# Properly convert environment variables
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
```

### 7. Provide Defaults

```python
# Sensible defaults for optional configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
WORKERS = int(os.getenv("WORKERS", "1"))
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "false").lower() == "true"
```

## Troubleshooting

### Configuration Not Loading

**Check environment variables:**
```bash
# Docker
docker exec choreoai env | grep -i api_key

# Kubernetes
kubectl exec choreoai-pod -- env | grep -i api_key
```

**Verify file permissions:**
```bash
ls -la .env
# Should be readable by the application user
```

### Invalid Configuration Values

**Check logs:**
```bash
# Look for configuration errors
docker logs choreoai 2>&1 | grep -i "config\|error"
```

**Validate values:**
```bash
# Test configuration
curl http://localhost:8000/v1/config/validate
```

### Provider Connection Issues

**Test provider connectivity:**
```bash
# OpenAI
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Anthropic
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### CORS Issues

**Check allowed origins:**
```bash
# Test CORS
curl -H "Origin: https://example.com" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     http://localhost:8000/v1/chat/completions
```

**Update configuration:**
```bash
# Add specific origin
ALLOWED_ORIGINS=https://example.com,https://app.example.com
```

### Rate Limiting Problems

**Check rate limit settings:**
```bash
echo $RATE_LIMIT_ENABLED
echo $RATE_LIMIT_REQUESTS
```

**Disable for testing:**
```bash
RATE_LIMIT_ENABLED=false
```

### Secret Not Found

**Kubernetes secret:**
```bash
# Check if secret exists
kubectl get secret choreoai-secrets -n choreoai

# View secret keys (not values)
kubectl describe secret choreoai-secrets -n choreoai

# Decode secret
kubectl get secret choreoai-secrets -n choreoai \
  -o jsonpath='{.data.OPENAI_API_KEY}' | base64 -d
```

## Next Steps

1. **Deploy**: Choose your deployment method - [Docker](docker.md), [Kubernetes](kubernetes.md), or [Helm](helm.md)
2. **Monitor**: Set up [Monitoring](monitoring.md) for production visibility
3. **Secure**: Implement security best practices
4. **Optimize**: Fine-tune performance settings for your workload

## Additional Resources

- [12-Factor App Configuration](https://12factor.net/config)
- [Environment Variable Best Practices](https://blog.stackpath.com/environment-variables/)
- [Secrets Management Guide](https://www.vaultproject.io/docs/what-is-vault)
- [ChoreoAI GitHub Repository](https://github.com/choreoai/choreoai)
