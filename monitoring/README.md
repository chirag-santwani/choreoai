# ChoreoAI Monitoring Stack

This directory contains the complete monitoring infrastructure for ChoreoAI, including Prometheus, Grafana, AlertManager, and Jaeger.

## Overview

The monitoring stack provides:
- **Prometheus** - Metrics collection and storage
- **Grafana** - Metrics visualization and dashboards
- **AlertManager** - Alert routing and notification management
- **Jaeger** - Distributed tracing (optional)

## Quick Start

### Start the Monitoring Stack

From the project root directory:

```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

This will start:
- ChoreoAI API on `http://localhost:8000`
- Prometheus on `http://localhost:9090`
- Grafana on `http://localhost:3000`
- AlertManager on `http://localhost:9093`
- Jaeger UI on `http://localhost:16686`

### Access the Services

1. **Grafana Dashboard**
   - URL: http://localhost:3000
   - Default credentials: `admin` / `admin`
   - Pre-configured dashboard: "ChoreoAI Overview"

2. **Prometheus**
   - URL: http://localhost:9090
   - Query metrics directly
   - View alert rules and targets

3. **AlertManager**
   - URL: http://localhost:9093
   - View active alerts
   - Configure notification receivers

4. **Jaeger (Tracing)**
   - URL: http://localhost:16686
   - View distributed traces
   - Analyze request flows

5. **ChoreoAI Metrics**
   - Metrics endpoint: http://localhost:8000/metrics
   - Health check: http://localhost:8000/health

## Available Metrics

ChoreoAI exposes the following Prometheus metrics:

### Request Metrics
- `choreoai_requests_total` - Total API requests (by provider, model, endpoint, status, method)
- `choreoai_request_duration_seconds` - Request duration histogram (by provider, endpoint, method)
- `choreoai_streaming_requests_total` - Total streaming requests (by provider, model)

### Token Metrics
- `choreoai_tokens_total` - Total tokens processed (by provider, model, type: input/output)

### Error Metrics
- `choreoai_errors_total` - Total errors (by provider, error_type, endpoint)

### System Metrics
- `choreoai_active_connections` - Current active connections (gauge)

## Example Queries

### Request Rate
```promql
rate(choreoai_requests_total[5m])
```

### Error Rate Percentage
```promql
(rate(choreoai_errors_total[5m]) / rate(choreoai_requests_total[5m])) * 100
```

### P95 Latency
```promql
histogram_quantile(0.95, rate(choreoai_request_duration_seconds_bucket[5m]))
```

### Token Usage by Provider
```promql
sum by (provider) (rate(choreoai_tokens_total[5m]))
```

### Success Rate
```promql
(sum(rate(choreoai_requests_total{status=~"2.."}[5m])) / sum(rate(choreoai_requests_total[5m]))) * 100
```

## Alert Rules

Pre-configured alerts include:

1. **HighErrorRate** - Error rate > 5% for 5 minutes
2. **ServiceDown** - API service is down for 2 minutes
3. **HighLatency** - P95 latency > 5 seconds for 5 minutes
4. **VeryHighLatency** - P99 latency > 10 seconds for 5 minutes
5. **RateLimitApproaching** - Request rate > 80 req/sec for 5 minutes
6. **HighActiveConnections** - Active connections > 100 for 10 minutes
7. **ProviderHighErrorRate** - Provider error rate > 10% for 5 minutes
8. **NoRequestsReceived** - No requests in last 10 minutes
9. **HighTokenUsage** - Token usage > 1M tokens/hour

## Configuration

### Prometheus Configuration

Located at `prometheus/prometheus.yml`:
- Scrape interval: 15 seconds
- Scrapes metrics from ChoreoAI API at `/metrics`
- Loads alert rules from `prometheus/alerts.yml`

### AlertManager Configuration

Located at `alertmanager/alertmanager.yml`:
- Configure notification receivers (Slack, PagerDuty, Email, etc.)
- Customize alert routing rules
- Set up inhibition rules

Example Slack configuration:
```yaml
receivers:
  - name: 'slack-alerts'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        channel: '#choreoai-alerts'
        title: '🚨 ChoreoAI Alert'
        text: '{{ range .Alerts }}{{ .Annotations.description }}\n{{ end }}'
```

### Grafana Configuration

- Datasources: `grafana/provisioning/datasources/`
- Dashboard provisioning: `grafana/provisioning/dashboards/`
- Dashboards: `grafana/dashboards/`

## Customization

### Adding Custom Metrics

Edit `api/app/middleware/metrics.py` to add new Prometheus metrics:

```python
from prometheus_client import Counter, Histogram, Gauge

custom_metric = Counter(
    'choreoai_custom_metric',
    'Description of custom metric',
    ['label1', 'label2']
)
```

### Creating Custom Dashboards

1. Create dashboards in Grafana UI
2. Export as JSON
3. Save to `monitoring/grafana/dashboards/`
4. Restart Grafana container

### Adding Alert Rules

Edit `prometheus/alerts.yml`:

```yaml
- alert: CustomAlert
  expr: your_metric > threshold
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Alert summary"
    description: "Alert description"
```

## Logging

ChoreoAI uses structured JSON logging. View logs:

```bash
# View API logs
docker-compose -f docker-compose.monitoring.yml logs -f api

# Example log output
{
  "timestamp": "2024-01-15T10:30:00.123456",
  "level": "INFO",
  "logger": "choreoai",
  "message": "Request completed",
  "request_id": "abc123",
  "method": "POST",
  "path": "/v1/chat/completions",
  "status_code": 200,
  "duration": 1.234,
  "provider": "openai",
  "model": "gpt-4"
}
```

## Troubleshooting

### Metrics Not Appearing

1. Check if metrics endpoint is accessible:
   ```bash
   curl http://localhost:8000/metrics
   ```

2. Check Prometheus targets:
   - Visit http://localhost:9090/targets
   - Ensure ChoreoAI target is "UP"

3. Check logs:
   ```bash
   docker-compose -f docker-compose.monitoring.yml logs prometheus
   ```

### Alerts Not Firing

1. Check alert rules in Prometheus:
   - Visit http://localhost:9090/alerts
   - Verify rules are loaded

2. Check AlertManager:
   - Visit http://localhost:9093
   - Verify configuration is correct

3. Test alert:
   ```bash
   # Send test alert
   curl -X POST http://localhost:9093/api/v1/alerts -d '[{"labels":{"alertname":"test"}}]'
   ```

### Grafana Dashboard Not Loading

1. Check datasource connection:
   - Grafana → Configuration → Data Sources
   - Test Prometheus connection

2. Check dashboard provisioning:
   ```bash
   docker-compose -f docker-compose.monitoring.yml logs grafana
   ```

### High Memory Usage

1. Adjust Prometheus retention:
   ```yaml
   # In docker-compose.monitoring.yml
   command:
     - '--storage.tsdb.retention.time=15d'  # Reduce from default
   ```

2. Reduce scrape frequency:
   ```yaml
   # In prometheus/prometheus.yml
   scrape_interval: 30s  # Increase from 15s
   ```

## Stopping the Stack

```bash
docker-compose -f docker-compose.monitoring.yml down
```

To also remove volumes:
```bash
docker-compose -f docker-compose.monitoring.yml down -v
```

## Production Deployment

For production deployments:

1. **Secure Grafana**
   - Change default admin password
   - Enable HTTPS
   - Configure authentication (OAuth, LDAP, etc.)

2. **Configure AlertManager**
   - Set up proper notification channels
   - Configure on-call rotations
   - Test alert delivery

3. **Persistent Storage**
   - Use named volumes or external storage
   - Regular backups of Prometheus data

4. **Resource Limits**
   - Set memory/CPU limits in docker-compose
   - Monitor resource usage

5. **High Availability**
   - Run multiple Prometheus instances
   - Use Thanos for long-term storage
   - Deploy AlertManager in HA mode

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [AlertManager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [ChoreoAI Monitoring Documentation](../docs/deployment/monitoring.md)
