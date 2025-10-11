# Monitoring and Observability

This guide covers monitoring, logging, and observability best practices for ChoreoAI in production environments.

## Table of Contents

- [Overview](#overview)
- [Health Checks](#health-checks)
- [Metrics Collection](#metrics-collection)
- [Logging](#logging)
- [Tracing](#tracing)
- [Alerting](#alerting)
- [Dashboard Examples](#dashboard-examples)
- [Troubleshooting](#troubleshooting)

## Overview

Proper monitoring is essential for maintaining reliable ChoreoAI deployments. This guide covers:

- **Health Checks**: Endpoint monitoring and readiness probes
- **Metrics**: Performance and usage metrics collection
- **Logging**: Structured logging and log aggregation
- **Tracing**: Distributed tracing for request flows
- **Alerting**: Setting up alerts for critical issues

## Health Checks

### Built-in Health Endpoint

ChoreoAI provides a `/health` endpoint for monitoring:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Kubernetes Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

### Kubernetes Readiness Probe

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 2
```

### Docker Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

## Metrics Collection

### Prometheus Integration

ChoreoAI can expose metrics in Prometheus format:

#### 1. Install Prometheus Python Client

```bash
pip install prometheus-client
```

#### 2. Configure Metrics Endpoint

Add to your FastAPI app:

```python
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response

# Define metrics
request_count = Counter(
    'choreoai_requests_total',
    'Total number of requests',
    ['provider', 'model', 'status']
)

request_duration = Histogram(
    'choreoai_request_duration_seconds',
    'Request duration in seconds',
    ['provider', 'model']
)

@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
```

#### 3. Prometheus Configuration

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'choreoai'
    static_configs:
      - targets: ['choreoai:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

### Key Metrics to Track

#### Request Metrics
- `choreoai_requests_total` - Total requests by provider/model
- `choreoai_request_duration_seconds` - Request latency
- `choreoai_errors_total` - Error count by type
- `choreoai_streaming_requests_total` - Streaming requests

#### Provider Metrics
- `choreoai_provider_requests_total` - Requests per provider
- `choreoai_provider_errors_total` - Provider-specific errors
- `choreoai_provider_latency_seconds` - Provider response times

#### Token Metrics
- `choreoai_tokens_processed_total` - Total tokens (input/output)
- `choreoai_estimated_cost_total` - Estimated API costs

#### System Metrics
- `choreoai_active_connections` - Current active connections
- `choreoai_queue_size` - Request queue depth

### Example Metrics Implementation

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Request metrics
request_counter = Counter(
    'choreoai_requests_total',
    'Total API requests',
    ['provider', 'model', 'endpoint', 'status']
)

request_histogram = Histogram(
    'choreoai_request_duration_seconds',
    'Request duration',
    ['provider', 'endpoint']
)

# Token metrics
token_counter = Counter(
    'choreoai_tokens_total',
    'Total tokens processed',
    ['provider', 'model', 'type']  # type: input/output
)

# Error metrics
error_counter = Counter(
    'choreoai_errors_total',
    'Total errors',
    ['provider', 'error_type']
)

# Active connections
active_connections = Gauge(
    'choreoai_active_connections',
    'Current active connections'
)

# Usage in middleware
@app.middleware("http")
async def metrics_middleware(request, call_next):
    active_connections.inc()
    start_time = time.time()

    try:
        response = await call_next(request)
        duration = time.time() - start_time

        # Record metrics
        request_counter.labels(
            provider=request.state.provider,
            model=request.state.model,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()

        request_histogram.labels(
            provider=request.state.provider,
            endpoint=request.url.path
        ).observe(duration)

        return response
    except Exception as e:
        error_counter.labels(
            provider=getattr(request.state, 'provider', 'unknown'),
            error_type=type(e).__name__
        ).inc()
        raise
    finally:
        active_connections.dec()
```

## Logging

### Structured Logging Configuration

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add extra fields
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        if hasattr(record, 'provider'):
            log_data['provider'] = record.provider
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id

        return json.dumps(log_data)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("choreoai")
logger.handlers[0].setFormatter(JSONFormatter())
```

### Request Logging Middleware

```python
import uuid
from fastapi import Request

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    logger.info(
        "Request started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host
        }
    )

    try:
        response = await call_next(request)

        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "provider": getattr(request.state, 'provider', None)
            }
        )

        response.headers["X-Request-ID"] = request_id
        return response

    except Exception as e:
        logger.error(
            "Request failed",
            extra={
                "request_id": request_id,
                "error": str(e),
                "error_type": type(e).__name__
            },
            exc_info=True
        )
        raise
```

### Log Levels

```python
# DEBUG - Detailed diagnostic information
logger.debug("Provider request details", extra={
    "provider": "openai",
    "model": "gpt-4",
    "tokens": 150
})

# INFO - General informational messages
logger.info("Chat completion request", extra={
    "provider": "openai",
    "model": "gpt-4"
})

# WARNING - Warning messages for potential issues
logger.warning("Provider rate limit approaching", extra={
    "provider": "openai",
    "remaining_requests": 10
})

# ERROR - Error messages for failures
logger.error("Provider request failed", extra={
    "provider": "openai",
    "error": "Connection timeout"
})

# CRITICAL - Critical issues requiring immediate attention
logger.critical("Database connection lost", extra={
    "database": "postgres"
})
```

### ELK Stack Integration

#### Filebeat Configuration

```yaml
# filebeat.yml
filebeat.inputs:
  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'
    processors:
      - add_kubernetes_metadata:
          host: ${NODE_NAME}
          matchers:
          - logs_path:
              logs_path: "/var/lib/docker/containers/"

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "choreoai-logs-%{+yyyy.MM.dd}"
```

#### Logstash Pipeline

```ruby
# logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  json {
    source => "message"
  }

  date {
    match => ["timestamp", "ISO8601"]
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "choreoai-logs-%{+YYYY.MM.dd}"
  }
}
```

## Tracing

### OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Initialize tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4317",
    insecure=True
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)
```

### Custom Spans

```python
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    with tracer.start_as_current_span("chat_completion") as span:
        span.set_attribute("provider", request.provider)
        span.set_attribute("model", request.model)

        with tracer.start_as_current_span("provider_request"):
            response = await adapter.chat_completion(request)
            span.set_attribute("tokens_used", response.usage.total_tokens)

        return response
```

### Jaeger Configuration

```yaml
# docker-compose.yml
jaeger:
  image: jaegertracing/all-in-one:latest
  ports:
    - "16686:16686"  # UI
    - "4317:4317"    # OTLP gRPC
  environment:
    - COLLECTOR_OTLP_ENABLED=true
```

## Alerting

### Prometheus Alert Rules

```yaml
# alerts.yml
groups:
  - name: choreoai_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          rate(choreoai_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec"

      # Provider down
      - alert: ProviderDown
        expr: |
          up{job="choreoai"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "ChoreoAI service is down"
          description: "Service has been down for 2 minutes"

      # High latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            rate(choreoai_request_duration_seconds_bucket[5m])
          ) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High request latency"
          description: "P95 latency is {{ $value }} seconds"

      # Rate limit approaching
      - alert: RateLimitApproaching
        expr: |
          rate(choreoai_requests_total[1m]) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Approaching rate limit"
          description: "Request rate is {{ $value }} req/min"
```

### AlertManager Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'
    - match:
        severity: warning
      receiver: 'slack'

receivers:
  - name: 'default'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/...'
        channel: '#choreoai-alerts'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: 'your-pagerduty-key'

  - name: 'slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/...'
        channel: '#choreoai-warnings'
```

## Dashboard Examples

### Grafana Dashboard - Overview

```json
{
  "dashboard": {
    "title": "ChoreoAI Overview",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(choreoai_requests_total[5m])"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(choreoai_errors_total[5m])"
          }
        ],
        "type": "graph"
      },
      {
        "title": "P95 Latency",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(choreoai_request_duration_seconds_bucket[5m]))"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Active Connections",
        "targets": [
          {
            "expr": "choreoai_active_connections"
          }
        ],
        "type": "gauge"
      }
    ]
  }
}
```

### Key Dashboard Panels

#### 1. Request Overview
- Total requests per minute
- Requests by provider
- Requests by model
- Success/error ratio

#### 2. Performance Metrics
- Average response time
- P50, P95, P99 latency
- Throughput (requests/sec)
- Queue depth

#### 3. Provider Health
- Provider availability
- Provider error rates
- Provider response times
- Rate limit status

#### 4. Resource Usage
- CPU utilization
- Memory usage
- Network I/O
- Disk usage

#### 5. Cost Tracking
- Tokens processed
- Estimated costs by provider
- Cost per request
- Daily/monthly spend

## Troubleshooting

### Common Issues

#### High Memory Usage

```bash
# Check memory usage
kubectl top pods -n choreoai

# Investigate with metrics
curl http://localhost:8000/metrics | grep memory
```

**Solutions**:
- Increase memory limits
- Implement connection pooling
- Add request rate limiting

#### Slow Responses

```bash
# Check latency metrics
curl http://localhost:8000/metrics | grep duration
```

**Solutions**:
- Check provider API status
- Verify network connectivity
- Review timeout settings
- Scale horizontally

#### High Error Rates

```bash
# Check error logs
kubectl logs -n choreoai deployment/choreoai --tail=100 | grep ERROR
```

**Solutions**:
- Verify provider API keys
- Check rate limits
- Review provider status pages
- Implement retries with backoff

### Debugging Tools

```python
# Enable debug logging
import logging
logging.getLogger("choreoai").setLevel(logging.DEBUG)

# Request tracing
curl -H "X-Debug: true" http://localhost:8000/v1/chat/completions
```

## Best Practices

1. **Set Up Comprehensive Monitoring**
   - Monitor all critical metrics
   - Set appropriate alert thresholds
   - Test alerting regularly

2. **Use Structured Logging**
   - Include request IDs
   - Log provider information
   - Track token usage

3. **Implement Distributed Tracing**
   - Trace across services
   - Track provider latencies
   - Identify bottlenecks

4. **Create Useful Dashboards**
   - Overview dashboard for health
   - Detailed dashboards per provider
   - Cost tracking dashboard

5. **Test Alert Rules**
   - Validate alert conditions
   - Avoid alert fatigue
   - Ensure actionable alerts

6. **Regular Reviews**
   - Review metrics weekly
   - Analyze trends monthly
   - Optimize based on data

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [ELK Stack Guide](https://www.elastic.co/guide/)

## Next Steps

- **[Configuration Guide](configuration.md)** - Configure deployment settings
- **[Kubernetes Deployment](kubernetes.md)** - Deploy to Kubernetes
- **[Docker Deployment](docker.md)** - Run with Docker
