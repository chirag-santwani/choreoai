# Deployment

Deploy ChoreoAI to production environments using Docker, Kubernetes, or Helm.

## Deployment Options

### Docker
**Best for:** Simple deployments, development, single-node production

Deploy ChoreoAI as a Docker container for easy portability and consistent environments.

**[Docker Deployment Guide →](docker.md)**

### Kubernetes
**Best for:** Cloud-native deployments, auto-scaling, high availability

Deploy to Kubernetes for enterprise-grade orchestration and scalability.

**[Kubernetes Deployment Guide →](kubernetes.md)**

### Helm
**Best for:** Simplified Kubernetes deployments, configuration management

Use Helm charts for streamlined Kubernetes deployments with customizable values.

**[Helm Deployment Guide →](helm.md)**

## Quick Start

### Docker (Fastest)

```bash
# Pull image
docker pull choreoai/choreoai:latest

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  --name choreoai \
  choreoai/choreoai:latest
```

### Kubernetes

```bash
# Create namespace
kubectl create namespace choreoai

# Create secrets
kubectl create secret generic choreoai-secrets \
  --from-literal=OPENAI_API_KEY=sk-... \
  --from-literal=ANTHROPIC_API_KEY=sk-ant-... \
  -n choreoai

# Deploy
kubectl apply -f deployment.yaml -n choreoai
```

### Helm

```bash
# Add repository
helm repo add choreoai https://charts.choreoai.io

# Install
helm install choreoai choreoai/choreoai \
  --set secrets.openai_api_key=sk-... \
  --set secrets.anthropic_api_key=sk-ant-...
```

## Prerequisites

### All Deployments
- API keys for desired providers (OpenAI, Claude, Azure, Gemini)
- Network access to provider APIs
- SSL certificates (for production)

### Docker
- Docker 20.10+ installed
- Docker Compose 2.0+ (optional)

### Kubernetes
- Kubernetes cluster 1.21+
- kubectl configured
- Sufficient cluster resources (2 CPU, 4GB RAM minimum)

### Helm
- Helm 3.0+ installed
- Kubernetes cluster access
- kubectl configured

## Choosing a Deployment Method

| Method | Complexity | Scalability | Best For |
|--------|------------|-------------|----------|
| Docker | Low | Limited | Development, small production |
| Kubernetes | High | Excellent | Enterprise, cloud-native |
| Helm | Medium | Excellent | Kubernetes with easy config |

## Architecture

### Basic Architecture
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  ChoreoAI   │
│   (API)     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  Provider APIs               │
│  (OpenAI, Claude, etc.)     │
└─────────────────────────────┘
```

### Production Architecture
```
┌──────────┐
│  Client  │
└────┬─────┘
     │
     ▼
┌──────────────┐
│ Load Balancer│
└──────┬───────┘
       │
       ▼
┌────────────────────┐
│  ChoreoAI Pods     │
│  (Auto-scaled)     │
└─────────┬──────────┘
          │
          ▼
┌─────────────────────┐
│  Provider APIs      │
└─────────────────────┘
```

## Environment Variables

All deployment methods require provider API keys:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | No* | OpenAI API key |
| `ANTHROPIC_API_KEY` | No* | Anthropic (Claude) API key |
| `AZURE_OPENAI_API_KEY` | No* | Azure OpenAI API key |
| `AZURE_OPENAI_ENDPOINT` | No | Azure OpenAI endpoint URL |
| `GEMINI_API_KEY` | No* | Google Gemini API key |
| `PORT` | No | Server port (default: 8000) |
| `HOST` | No | Server host (default: 0.0.0.0) |
| `LOG_LEVEL` | No | Logging level (default: info) |

*At least one provider API key is required.

See [Configuration Guide](configuration.md) for complete details.

## Security Considerations

### 1. API Key Management

!!! warning
    Never commit API keys to version control

**Recommended approaches:**
- Use Kubernetes Secrets
- Use external secret managers (AWS Secrets Manager, HashiCorp Vault)
- Use environment variable injection

### 2. Network Security

- Use HTTPS/TLS in production
- Implement API authentication
- Restrict network access with firewall rules
- Use private networks when possible

### 3. Container Security

- Use official images
- Scan images for vulnerabilities
- Run containers as non-root user
- Keep images updated

## Production Checklist

### Before Deployment

- [ ] Provider API keys configured
- [ ] SSL/TLS certificates ready
- [ ] Monitoring solution selected
- [ ] Logging configured
- [ ] Backup strategy defined
- [ ] Resource limits set
- [ ] Health checks configured
- [ ] API authentication enabled

### After Deployment

- [ ] Health endpoint accessible
- [ ] Test chat completion request
- [ ] Verify provider connectivity
- [ ] Check logs for errors
- [ ] Monitor resource usage
- [ ] Test failover scenarios
- [ ] Verify auto-scaling (if enabled)
- [ ] Set up alerts

## Resource Requirements

### Minimum (Development)
- **CPU**: 1 core
- **Memory**: 2 GB RAM
- **Storage**: 5 GB

### Recommended (Production)
- **CPU**: 2-4 cores
- **Memory**: 4-8 GB RAM
- **Storage**: 20 GB
- **Network**: Low latency to provider APIs

### High-Traffic (Enterprise)
- **CPU**: 4-8 cores per pod
- **Memory**: 8-16 GB RAM per pod
- **Storage**: 50 GB
- **Replicas**: 3-10 pods
- **Network**: Dedicated egress

## Scaling

### Vertical Scaling
Increase resources per instance:

**Docker:**
```bash
docker run -d \
  --cpus="4" \
  --memory="8g" \
  choreoai/choreoai:latest
```

**Kubernetes:**
```yaml
resources:
  requests:
    cpu: 2
    memory: 4Gi
  limits:
    cpu: 4
    memory: 8Gi
```

### Horizontal Scaling
Increase number of instances:

**Docker Compose:**
```bash
docker-compose up --scale choreoai=5
```

**Kubernetes:**
```bash
kubectl scale deployment choreoai --replicas=5
```

**Helm:**
```bash
helm upgrade choreoai choreoai/choreoai \
  --set replicaCount=5
```

## Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy"
}
```

### Metrics Endpoint

```bash
curl http://localhost:8000/metrics
```

See [Monitoring Guide](monitoring.md) for detailed setup.

## Common Deployment Patterns

### 1. Single Region

```
Region: us-east-1
├── Load Balancer
└── ChoreoAI (3 replicas)
```

### 2. Multi-Region

```
Region: us-east-1          Region: eu-west-1
├── Load Balancer          ├── Load Balancer
└── ChoreoAI (3 replicas)  └── ChoreoAI (3 replicas)
```

### 3. Hybrid Cloud

```
AWS                        On-Premise
├── ChoreoAI (Primary)    ├── ChoreoAI (Failover)
└── Provider Access       └── Local Processing
```

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker logs choreoai
kubectl logs -l app=choreoai -n choreoai
```

**Common issues:**
- Missing API keys
- Port already in use
- Insufficient resources

### Can't Connect to API

**Verify deployment:**
```bash
# Docker
docker ps | grep choreoai

# Kubernetes
kubectl get pods -n choreoai
```

**Test locally:**
```bash
curl http://localhost:8000/health
```

### Provider Errors

**Verify API keys:**
```bash
# Docker
docker exec choreoai env | grep API_KEY

# Kubernetes
kubectl get secret choreoai-secrets -n choreoai -o yaml
```

**Test provider access:**
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "test"}]}'
```

## Documentation

### Detailed Guides
- **[Docker Deployment](docker.md)** - Deploy with Docker
- **[Kubernetes Deployment](kubernetes.md)** - Deploy to Kubernetes
- **[Helm Deployment](helm.md)** - Deploy with Helm
- **[Configuration](configuration.md)** - Environment variables and settings
- **[Monitoring](monitoring.md)** - Observability and monitoring

### Related
- **[API Reference](../api/README.md)** - API documentation
- **[Providers](../providers/README.md)** - Configure providers

## Next Steps

1. **Choose deployment method** based on your requirements
2. **Configure environment variables** for your providers
3. **Deploy using your chosen method** (Docker/Kubernetes/Helm)
4. **Set up monitoring** for production visibility
5. **Test the deployment** with sample requests
