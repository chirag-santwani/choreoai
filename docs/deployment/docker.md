# Docker Deployment

Deploy ChoreoAI using Docker for easy portability and consistent environments across development and production.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Building from Source](#building-from-source)
- [Using Pre-built Images](#using-pre-built-images)
- [Docker Compose](#docker-compose)
- [Configuration](#configuration)
- [Networking](#networking)
- [Volumes and Persistence](#volumes-and-persistence)
- [Security](#security)
- [Resource Management](#resource-management)
- [Health Checks](#health-checks)
- [Logging](#logging)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Docker provides a lightweight, portable way to deploy ChoreoAI. This guide covers:

- Single container deployment
- Multi-container deployment with Docker Compose
- Production configurations
- Security hardening
- Performance optimization

### When to Use Docker

| Scenario | Recommended |
|----------|-------------|
| Local development | Yes |
| Testing and CI/CD | Yes |
| Single-node production | Yes |
| Small-scale production | Yes |
| Multi-node clusters | No (use Kubernetes) |
| Enterprise deployments | No (use Kubernetes/Helm) |

## Prerequisites

### Required

- Docker 20.10+ installed
- At least one AI provider API key
- 2GB RAM available
- 5GB disk space

### Optional

- Docker Compose 2.0+ (for multi-container setups)
- Docker Buildx (for multi-platform builds)
- Docker registry access (for custom images)

### Installation

**macOS:**
```bash
brew install docker
```

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

**Verify installation:**
```bash
docker --version
docker-compose --version
```

## Quick Start

### 1. Pull and Run

```bash
# Pull the latest image
docker pull choreoai/choreoai:latest

# Run with environment variables
docker run -d \
  --name choreoai \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-openai-key \
  -e ANTHROPIC_API_KEY=sk-ant-your-anthropic-key \
  choreoai/choreoai:latest

# Test the deployment
curl http://localhost:8000/health
```

### 2. Using Environment File

```bash
# Create environment file
cat > .env << EOF
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GEMINI_API_KEY=your-gemini-key
LOG_LEVEL=INFO
EOF

# Run with environment file
docker run -d \
  --name choreoai \
  -p 8000:8000 \
  --env-file .env \
  choreoai/choreoai:latest
```

### 3. Verify Deployment

```bash
# Check container status
docker ps | grep choreoai

# View logs
docker logs choreoai

# Test API
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Building from Source

### Basic Build

```bash
# Clone repository
git clone https://github.com/choreoai/choreoai.git
cd choreoai/api

# Build image
docker build -t choreoai:local .

# Run locally built image
docker run -d \
  --name choreoai \
  -p 8000:8000 \
  --env-file .env \
  choreoai:local
```

### Multi-stage Build

The Dockerfile uses multi-stage builds for optimization:

```dockerfile
# Stage 1: Builder - Install dependencies
FROM python:3.11-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y gcc
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production - Minimal runtime
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl
RUN useradd -m -u 1000 choreoai
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --chown=choreoai:choreoai ./app ./app
USER choreoai
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Custom Build Arguments

```bash
# Build with specific Python version
docker build \
  --build-arg PYTHON_VERSION=3.11 \
  -t choreoai:py311 \
  .

# Build with development dependencies
docker build \
  --build-arg BUILD_ENV=development \
  -t choreoai:dev \
  .
```

### Multi-platform Builds

```bash
# Enable buildx
docker buildx create --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t choreoai/choreoai:latest \
  --push \
  .
```

## Using Pre-built Images

### Available Tags

| Tag | Description | Use Case |
|-----|-------------|----------|
| `latest` | Latest stable release | Production |
| `v1.2.3` | Specific version | Production (pinned) |
| `develop` | Development branch | Testing |
| `nightly` | Nightly builds | Testing |

### Pull Specific Version

```bash
# Pull specific version
docker pull choreoai/choreoai:v1.2.3

# Run specific version
docker run -d \
  --name choreoai \
  -p 8000:8000 \
  --env-file .env \
  choreoai/choreoai:v1.2.3
```

### Image Size Comparison

| Image Type | Size | Build Time |
|------------|------|------------|
| Full | ~800MB | 5-10 min |
| Slim | ~400MB | 3-5 min |
| Alpine | ~200MB | 8-12 min |

## Docker Compose

### Basic Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  choreoai:
    image: choreoai/choreoai:latest
    container_name: choreoai-api
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - HOST=0.0.0.0
      - LOG_LEVEL=INFO
      - ENVIRONMENT=production
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Start Services

```bash
# Start in foreground
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Configuration

```yaml
version: '3.8'

services:
  choreoai:
    image: choreoai/choreoai:v1.2.3
    container_name: choreoai-api
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - HOST=0.0.0.0
      - LOG_LEVEL=WARNING
      - ENVIRONMENT=production
      - ALLOWED_ORIGINS=https://yourdomain.com
    env_file:
      - .env.production
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - choreoai-network

networks:
  choreoai-network:
    driver: bridge
```

### Scaling with Compose

```bash
# Scale to 3 instances
docker-compose up -d --scale choreoai=3

# With load balancer
docker-compose -f docker-compose.lb.yml up -d
```

Example `docker-compose.lb.yml`:

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - choreoai
    networks:
      - choreoai-network

  choreoai:
    image: choreoai/choreoai:latest
    environment:
      - PORT=8000
    env_file:
      - .env
    expose:
      - "8000"
    networks:
      - choreoai-network

networks:
  choreoai-network:
    driver: bridge
```

## Configuration

### Environment Variables

All configuration is done via environment variables:

```bash
# Server Configuration
PORT=8000                    # Server port
HOST=0.0.0.0                 # Server host
LOG_LEVEL=INFO              # Logging level
ENVIRONMENT=production      # Environment name
ALLOWED_ORIGINS=*           # CORS origins

# Provider API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_API_KEY=...
GEMINI_API_KEY=...
GROK_API_KEY=...

# AWS (for Bedrock)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

See [Configuration Reference](configuration.md) for complete details.

### Secrets Management

**Using Docker Secrets:**

```bash
# Create secrets
echo "sk-your-key" | docker secret create openai_key -
echo "sk-ant-your-key" | docker secret create anthropic_key -

# Use in docker-compose.yml
version: '3.8'

services:
  choreoai:
    image: choreoai/choreoai:latest
    secrets:
      - openai_key
      - anthropic_key
    environment:
      - OPENAI_API_KEY_FILE=/run/secrets/openai_key
      - ANTHROPIC_API_KEY_FILE=/run/secrets/anthropic_key

secrets:
  openai_key:
    external: true
  anthropic_key:
    external: true
```

## Networking

### Port Mapping

```bash
# Map to different host port
docker run -d \
  -p 3000:8000 \
  choreoai/choreoai:latest

# Map to specific interface
docker run -d \
  -p 127.0.0.1:8000:8000 \
  choreoai/choreoai:latest
```

### Custom Networks

```bash
# Create network
docker network create choreoai-net

# Run with custom network
docker run -d \
  --name choreoai \
  --network choreoai-net \
  -p 8000:8000 \
  choreoai/choreoai:latest

# Connect another container
docker run -d \
  --name nginx \
  --network choreoai-net \
  -p 80:80 \
  nginx:alpine
```

### Network Modes

| Mode | Use Case | Security |
|------|----------|----------|
| bridge | Default, isolated | Medium |
| host | Better performance | Low |
| none | Maximum isolation | High |
| custom | Production networks | High |

## Volumes and Persistence

### Log Persistence

```bash
# Mount log directory
docker run -d \
  --name choreoai \
  -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  choreoai/choreoai:latest
```

### Configuration Files

```bash
# Mount configuration
docker run -d \
  --name choreoai \
  -p 8000:8000 \
  -v $(pwd)/config:/app/config:ro \
  choreoai/choreoai:latest
```

### Volume Best Practices

```yaml
services:
  choreoai:
    image: choreoai/choreoai:latest
    volumes:
      # Named volume for logs
      - choreoai-logs:/app/logs
      # Read-only config
      - ./config:/app/config:ro
      # Bind mount for development
      - ./app:/app:delegated

volumes:
  choreoai-logs:
    driver: local
```

## Security

### Running as Non-Root

The official image runs as non-root user (UID 1000):

```bash
# Verify user
docker run --rm choreoai/choreoai:latest id
# Output: uid=1000(choreoai) gid=1000(choreoai)
```

### Security Options

```bash
# Run with security options
docker run -d \
  --name choreoai \
  --read-only \
  --tmpfs /tmp \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  --security-opt no-new-privileges:true \
  -p 8000:8000 \
  choreoai/choreoai:latest
```

### Scanning for Vulnerabilities

```bash
# Scan image with Docker Scout
docker scout cves choreoai/choreoai:latest

# Scan with Trivy
trivy image choreoai/choreoai:latest

# Scan with Snyk
snyk container test choreoai/choreoai:latest
```

### Security Checklist

- [ ] Use specific version tags, not `latest`
- [ ] Run as non-root user
- [ ] Use read-only filesystem where possible
- [ ] Drop unnecessary capabilities
- [ ] Scan images for vulnerabilities
- [ ] Use secrets management
- [ ] Enable TLS/HTTPS
- [ ] Implement network policies
- [ ] Regular security updates

## Resource Management

### CPU and Memory Limits

```bash
# Set resource limits
docker run -d \
  --name choreoai \
  --cpus="2" \
  --memory="4g" \
  --memory-swap="4g" \
  -p 8000:8000 \
  choreoai/choreoai:latest
```

### Resource Reservations

```yaml
services:
  choreoai:
    image: choreoai/choreoai:latest
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
```

### Monitoring Resources

```bash
# Real-time stats
docker stats choreoai

# Detailed inspection
docker inspect choreoai | grep -A 10 "Memory"
```

### Resource Requirements

| Deployment Type | CPU | Memory | Disk |
|----------------|-----|--------|------|
| Development | 1 core | 2GB | 5GB |
| Small Production | 2 cores | 4GB | 10GB |
| Medium Production | 4 cores | 8GB | 20GB |
| Large Production | 8 cores | 16GB | 50GB |

## Health Checks

### Built-in Health Check

The image includes a health check:

```bash
# View health status
docker inspect --format='{{.State.Health.Status}}' choreoai

# View health check logs
docker inspect --format='{{json .State.Health}}' choreoai | jq
```

### Custom Health Check

```yaml
services:
  choreoai:
    image: choreoai/choreoai:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Manual Health Check

```bash
# Check health endpoint
curl http://localhost:8000/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2025-10-05T12:00:00Z"
}
```

## Logging

### View Logs

```bash
# Follow logs
docker logs -f choreoai

# Last 100 lines
docker logs --tail 100 choreoai

# Logs since timestamp
docker logs --since 2025-10-05T10:00:00 choreoai

# Logs with timestamps
docker logs -t choreoai
```

### Log Drivers

```bash
# JSON file (default)
docker run -d \
  --name choreoai \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  choreoai/choreoai:latest

# Syslog
docker run -d \
  --name choreoai \
  --log-driver syslog \
  --log-opt syslog-address=tcp://192.168.0.42:514 \
  choreoai/choreoai:latest

# Fluentd
docker run -d \
  --name choreoai \
  --log-driver fluentd \
  --log-opt fluentd-address=localhost:24224 \
  choreoai/choreoai:latest
```

### Log Configuration

```yaml
services:
  choreoai:
    image: choreoai/choreoai:latest
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "production"
        env: "ENVIRONMENT"
```

## Best Practices

### 1. Use Specific Tags

```bash
# Bad - uses latest
docker pull choreoai/choreoai:latest

# Good - pins version
docker pull choreoai/choreoai:v1.2.3
```

### 2. Health Checks

Always include health checks for production:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### 3. Resource Limits

Set appropriate limits:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
```

### 4. Restart Policies

```bash
# Development
--restart no

# Production
--restart unless-stopped
# or
--restart always
```

### 5. Secrets Management

Never hardcode secrets:

```bash
# Bad
-e OPENAI_API_KEY=sk-actual-key

# Good
--env-file .env
# or
--secret openai_key
```

### 6. Multi-stage Builds

Use multi-stage builds to reduce image size:

```dockerfile
FROM python:3.11-slim as builder
# Build stage

FROM python:3.11-slim
# Production stage
```

### 7. Log Rotation

Configure log rotation:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 8. Network Isolation

Use custom networks:

```bash
docker network create --driver bridge choreoai-net
```

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker logs choreoai
```

**Common issues:**
- Missing required environment variables
- Port already in use
- Insufficient resources
- Invalid configuration

**Solutions:**
```bash
# Check port availability
lsof -i :8000

# Check resources
docker info | grep -A 5 "CPUs"

# Verify environment
docker exec choreoai env | grep API_KEY
```

### Cannot Connect to API

**Check container status:**
```bash
docker ps | grep choreoai
```

**Verify port mapping:**
```bash
docker port choreoai
```

**Test from inside container:**
```bash
docker exec choreoai curl http://localhost:8000/health
```

**Test from host:**
```bash
curl http://localhost:8000/health
```

### High Memory Usage

**Check current usage:**
```bash
docker stats choreoai
```

**Adjust memory limits:**
```bash
docker update --memory 4g choreoai
```

**Restart with new limits:**
```bash
docker stop choreoai
docker rm choreoai
docker run -d --memory="4g" ...
```

### Performance Issues

**Check resource constraints:**
```bash
docker inspect choreoai | grep -A 20 "Resources"
```

**Monitor performance:**
```bash
docker stats choreoai
```

**Solutions:**
- Increase CPU/memory limits
- Use host network mode for better performance
- Optimize application configuration
- Scale horizontally with multiple containers

### Image Pull Failures

**Check connectivity:**
```bash
docker pull hello-world
```

**Use specific registry:**
```bash
docker pull docker.io/choreoai/choreoai:latest
```

**Login to private registry:**
```bash
docker login
docker pull choreoai/choreoai:latest
```

### Container Crashes

**View crash logs:**
```bash
docker logs --tail 200 choreoai
```

**Check exit code:**
```bash
docker inspect choreoai | grep ExitCode
```

**Common exit codes:**
- 0: Success
- 1: Application error
- 137: Out of memory (OOM)
- 139: Segmentation fault

### Health Check Failures

**Manual health check:**
```bash
curl http://localhost:8000/health
```

**Check health logs:**
```bash
docker inspect --format='{{json .State.Health}}' choreoai | jq
```

**Adjust health check timing:**
```yaml
healthcheck:
  interval: 60s        # Increase interval
  start_period: 120s   # Increase start period
```

## Next Steps

1. **Production Deployment**: Review [Kubernetes](kubernetes.md) or [Helm](helm.md) for scalable deployments
2. **Configuration**: See [Configuration Reference](configuration.md) for all options
3. **Monitoring**: Set up [Monitoring](monitoring.md) for production visibility
4. **Security**: Implement security best practices
5. **Performance**: Optimize for your workload

## Additional Resources

- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [ChoreoAI GitHub Repository](https://github.com/choreoai/choreoai)
