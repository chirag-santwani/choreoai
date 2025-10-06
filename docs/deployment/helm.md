# Helm Deployment

Deploy ChoreoAI using Helm for simplified Kubernetes deployments with customizable configuration management.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Chart Structure](#chart-structure)
- [Configuration](#configuration)
- [Installation](#installation)
- [Upgrading](#upgrading)
- [Uninstallation](#uninstallation)
- [Values Reference](#values-reference)
- [Advanced Configuration](#advanced-configuration)
- [Multi-environment Deployments](#multi-environment-deployments)
- [Custom Values](#custom-values)
- [Hooks and Tests](#hooks-and-tests)
- [Chart Development](#chart-development)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Helm is the package manager for Kubernetes, providing:

- Simplified deployment with a single command
- Version management and rollbacks
- Templated configurations
- Dependency management
- Release lifecycle management

### When to Use Helm

| Scenario | Recommended |
|----------|-------------|
| Kubernetes deployments | Yes |
| Multiple environments (dev/staging/prod) | Yes |
| Complex configurations | Yes |
| Team collaboration | Yes |
| Simple Docker deployments | No |
| Non-Kubernetes environments | No |

## Prerequisites

### Required

- Kubernetes cluster 1.21+
- Helm 3.0+ installed
- kubectl configured
- At least one AI provider API key

### Optional

- Helm plugins (diff, secrets)
- GitOps tools (ArgoCD, Flux)
- Monitoring stack

### Installation

**macOS:**
```bash
brew install helm
```

**Linux:**
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

**Windows:**
```powershell
choco install kubernetes-helm
```

**Verify installation:**
```bash
helm version
```

## Quick Start

### 1. Add Helm Repository

```bash
# Add ChoreoAI Helm repository
helm repo add choreoai https://charts.choreoai.io

# Update repository
helm repo update

# Search for charts
helm search repo choreoai
```

### 2. Install Chart

```bash
# Install with default values
helm install choreoai choreoai/choreoai \
  --namespace choreoai \
  --create-namespace

# Install with custom values
helm install choreoai choreoai/choreoai \
  --namespace choreoai \
  --create-namespace \
  --set secrets.openai_api_key=sk-your-key \
  --set secrets.anthropic_api_key=sk-ant-your-key
```

### 3. Verify Installation

```bash
# Check release status
helm status choreoai -n choreoai

# List releases
helm list -n choreoai

# Get values
helm get values choreoai -n choreoai

# Check pods
kubectl get pods -n choreoai
```

### 4. Test Deployment

```bash
# Port forward
kubectl port-forward svc/choreoai 8000:80 -n choreoai

# Test API
curl http://localhost:8000/health
```

## Chart Structure

```
choreoai/
├── Chart.yaml                 # Chart metadata
├── values.yaml               # Default configuration values
├── values.schema.json        # JSON schema for values validation
├── README.md                 # Chart documentation
├── templates/                # Kubernetes manifest templates
│   ├── deployment.yaml       # Deployment template
│   ├── service.yaml          # Service template
│   ├── ingress.yaml          # Ingress template
│   ├── configmap.yaml        # ConfigMap template
│   ├── secret.yaml           # Secret template
│   ├── serviceaccount.yaml   # ServiceAccount template
│   ├── hpa.yaml              # HorizontalPodAutoscaler template
│   ├── pdb.yaml              # PodDisruptionBudget template
│   ├── networkpolicy.yaml    # NetworkPolicy template
│   ├── NOTES.txt             # Post-installation notes
│   └── _helpers.tpl          # Template helpers
├── charts/                   # Chart dependencies
└── .helmignore              # Files to ignore
```

## Configuration

### Chart.yaml

```yaml
apiVersion: v2
name: choreoai
description: A unified API orchestration platform for multiple AI providers
type: application
version: 1.2.3
appVersion: "1.2.3"
keywords:
  - ai
  - openai
  - claude
  - gemini
  - llm
  - api
home: https://choreoai.io
sources:
  - https://github.com/choreoai/choreoai
maintainers:
  - name: ChoreoAI Team
    email: support@choreoai.io
icon: https://choreoai.io/icon.png
```

### Default values.yaml

```yaml
# Number of replicas
replicaCount: 3

# Image configuration
image:
  repository: choreoai/choreoai
  pullPolicy: IfNotPresent
  tag: "v1.2.3"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

# Service account
serviceAccount:
  create: true
  annotations: {}
  name: ""

# Pod annotations
podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8000"
  prometheus.io/path: "/metrics"

# Pod security context
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

# Container security context
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
  capabilities:
    drop:
    - ALL

# Service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: 8000
  annotations: {}

# Ingress configuration
ingress:
  enabled: false
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: api.choreoai.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: choreoai-tls
      hosts:
        - api.choreoai.example.com

# Resource limits
resources:
  requests:
    cpu: 500m
    memory: 1Gi
  limits:
    cpu: 2000m
    memory: 4Gi

# Autoscaling
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

# Pod disruption budget
podDisruptionBudget:
  enabled: true
  minAvailable: 2

# Node selector
nodeSelector: {}

# Tolerations
tolerations: []

# Affinity
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app.kubernetes.io/name
            operator: In
            values:
            - choreoai
        topologyKey: kubernetes.io/hostname

# Liveness probe
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

# Readiness probe
readinessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

# Environment variables
env:
  PORT: "8000"
  HOST: "0.0.0.0"
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  ALLOWED_ORIGINS: "*"
  AWS_REGION: "us-east-1"

# Secrets (API keys)
secrets:
  openai_api_key: ""
  anthropic_api_key: ""
  azure_openai_api_key: ""
  azure_openai_endpoint: ""
  gemini_api_key: ""
  grok_api_key: ""
  aws_access_key_id: ""
  aws_secret_access_key: ""

# Existing secret (if you want to use external secret)
existingSecret: ""

# Network policy
networkPolicy:
  enabled: false
  policyTypes:
    - Ingress
    - Egress

# Monitoring
monitoring:
  enabled: false
  serviceMonitor:
    enabled: false
    interval: 30s
```

## Installation

### Basic Installation

```bash
# Install with default values
helm install choreoai choreoai/choreoai \
  --namespace choreoai \
  --create-namespace
```

### Installation with Values

```bash
# Install with values from file
helm install choreoai choreoai/choreoai \
  --namespace choreoai \
  --create-namespace \
  --values values-production.yaml

# Install with inline values
helm install choreoai choreoai/choreoai \
  --namespace choreoai \
  --create-namespace \
  --set image.tag=v1.2.3 \
  --set replicaCount=5 \
  --set secrets.openai_api_key=sk-your-key
```

### Installation with Multiple Value Files

```bash
# Merge multiple value files
helm install choreoai choreoai/choreoai \
  --namespace choreoai \
  --create-namespace \
  --values values-common.yaml \
  --values values-production.yaml \
  --values values-secrets.yaml
```

### Dry Run

```bash
# Preview installation without applying
helm install choreoai choreoai/choreoai \
  --namespace choreoai \
  --dry-run \
  --debug

# Generate manifests
helm template choreoai choreoai/choreoai \
  --namespace choreoai \
  --values values-production.yaml > manifests.yaml
```

### Installation from Local Chart

```bash
# Package chart
helm package ./choreoai

# Install from package
helm install choreoai choreoai-1.2.3.tgz \
  --namespace choreoai \
  --create-namespace
```

## Upgrading

### Basic Upgrade

```bash
# Upgrade release
helm upgrade choreoai choreoai/choreoai \
  --namespace choreoai

# Upgrade with new values
helm upgrade choreoai choreoai/choreoai \
  --namespace choreoai \
  --values values-production.yaml
```

### Upgrade with Rollback on Failure

```bash
# Automatic rollback on failure
helm upgrade choreoai choreoai/choreoai \
  --namespace choreoai \
  --atomic \
  --timeout 10m
```

### Install or Upgrade

```bash
# Install if not exists, upgrade if exists
helm upgrade --install choreoai choreoai/choreoai \
  --namespace choreoai \
  --create-namespace \
  --values values-production.yaml
```

### Upgrade Specific Version

```bash
# Upgrade to specific chart version
helm upgrade choreoai choreoai/choreoai \
  --namespace choreoai \
  --version 1.2.3
```

### View Upgrade History

```bash
# List releases
helm history choreoai -n choreoai

# View specific revision
helm get values choreoai --revision 2 -n choreoai
```

### Rollback

```bash
# Rollback to previous version
helm rollback choreoai -n choreoai

# Rollback to specific revision
helm rollback choreoai 2 -n choreoai

# Rollback with cleanup
helm rollback choreoai -n choreoai --cleanup-on-fail
```

## Uninstallation

```bash
# Uninstall release
helm uninstall choreoai -n choreoai

# Uninstall and keep history
helm uninstall choreoai -n choreoai --keep-history

# Delete namespace
kubectl delete namespace choreoai
```

## Values Reference

### Complete Values Structure

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `3` |
| `image.repository` | Image repository | `choreoai/choreoai` |
| `image.tag` | Image tag | `v1.2.3` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `80` |
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.className` | Ingress class | `nginx` |
| `ingress.hosts` | Ingress hosts | `[]` |
| `resources.requests.cpu` | CPU request | `500m` |
| `resources.requests.memory` | Memory request | `1Gi` |
| `resources.limits.cpu` | CPU limit | `2000m` |
| `resources.limits.memory` | Memory limit | `4Gi` |
| `autoscaling.enabled` | Enable HPA | `true` |
| `autoscaling.minReplicas` | Min replicas | `3` |
| `autoscaling.maxReplicas` | Max replicas | `10` |
| `podDisruptionBudget.enabled` | Enable PDB | `true` |
| `podDisruptionBudget.minAvailable` | Min available pods | `2` |
| `secrets.openai_api_key` | OpenAI API key | `""` |
| `secrets.anthropic_api_key` | Anthropic API key | `""` |
| `env.LOG_LEVEL` | Logging level | `INFO` |
| `env.ENVIRONMENT` | Environment name | `production` |

### Environment-specific Values

**Development (values-dev.yaml):**
```yaml
replicaCount: 1

image:
  tag: "develop"
  pullPolicy: Always

env:
  LOG_LEVEL: "DEBUG"
  ENVIRONMENT: "development"

resources:
  requests:
    cpu: 250m
    memory: 512Mi
  limits:
    cpu: 500m
    memory: 1Gi

autoscaling:
  enabled: false

podDisruptionBudget:
  enabled: false

ingress:
  enabled: true
  hosts:
    - host: api-dev.choreoai.example.com
      paths:
        - path: /
          pathType: Prefix
```

**Staging (values-staging.yaml):**
```yaml
replicaCount: 2

image:
  tag: "v1.2.3-rc1"

env:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "staging"

resources:
  requests:
    cpu: 500m
    memory: 1Gi
  limits:
    cpu: 1000m
    memory: 2Gi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5

ingress:
  enabled: true
  hosts:
    - host: api-staging.choreoai.example.com
      paths:
        - path: /
          pathType: Prefix
```

**Production (values-production.yaml):**
```yaml
replicaCount: 5

image:
  tag: "v1.2.3"
  pullPolicy: IfNotPresent

env:
  LOG_LEVEL: "WARNING"
  ENVIRONMENT: "production"

resources:
  requests:
    cpu: 1000m
    memory: 2Gi
  limits:
    cpu: 4000m
    memory: 8Gi

autoscaling:
  enabled: true
  minReplicas: 5
  maxReplicas: 20
  targetCPUUtilizationPercentage: 60
  targetMemoryUtilizationPercentage: 70

podDisruptionBudget:
  enabled: true
  minAvailable: 3

affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: app.kubernetes.io/name
          operator: In
          values:
          - choreoai
      topologyKey: topology.kubernetes.io/zone

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
    - host: api.choreoai.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: choreoai-tls
      hosts:
        - api.choreoai.example.com

monitoring:
  enabled: true
  serviceMonitor:
    enabled: true
    interval: 30s

networkPolicy:
  enabled: true
```

## Advanced Configuration

### External Secrets

Using existing Kubernetes secret:

```yaml
# values.yaml
existingSecret: "choreoai-external-secrets"
secrets: {}
```

### Custom Environment Variables

```yaml
env:
  CUSTOM_VAR: "value"
  ANOTHER_VAR: "another-value"

# Or from ConfigMap
envFrom:
  - configMapRef:
      name: custom-config
```

### Extra Volumes

```yaml
extraVolumes:
  - name: custom-config
    configMap:
      name: custom-config

extraVolumeMounts:
  - name: custom-config
    mountPath: /app/config
    readOnly: true
```

### Init Containers

```yaml
initContainers:
  - name: wait-for-db
    image: busybox:1.28
    command: ['sh', '-c', 'until nc -z db 5432; do sleep 2; done']
```

### Sidecar Containers

```yaml
sidecars:
  - name: log-forwarder
    image: fluent/fluent-bit:latest
    volumeMounts:
      - name: logs
        mountPath: /logs
```

### Priority Class

```yaml
priorityClassName: high-priority
```

### Service Mesh Integration

**Istio:**
```yaml
podAnnotations:
  sidecar.istio.io/inject: "true"
  traffic.sidecar.istio.io/includeInboundPorts: "8000"
```

**Linkerd:**
```yaml
podAnnotations:
  linkerd.io/inject: enabled
```

## Multi-environment Deployments

### Using Separate Namespaces

```bash
# Development
helm upgrade --install choreoai choreoai/choreoai \
  --namespace choreoai-dev \
  --create-namespace \
  --values values-dev.yaml

# Staging
helm upgrade --install choreoai choreoai/choreoai \
  --namespace choreoai-staging \
  --create-namespace \
  --values values-staging.yaml

# Production
helm upgrade --install choreoai choreoai/choreoai \
  --namespace choreoai-prod \
  --create-namespace \
  --values values-production.yaml
```

### Environment-specific Secrets

```bash
# Create secrets per environment
kubectl create secret generic choreoai-secrets \
  --from-literal=OPENAI_API_KEY=sk-dev-key \
  -n choreoai-dev

kubectl create secret generic choreoai-secrets \
  --from-literal=OPENAI_API_KEY=sk-prod-key \
  -n choreoai-prod
```

### GitOps with ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: choreoai-production
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://charts.choreoai.io
    chart: choreoai
    targetRevision: 1.2.3
    helm:
      valueFiles:
        - values-production.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: choreoai-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Custom Values

### Secrets from File

```yaml
# secrets.yaml
secrets:
  openai_api_key: sk-your-openai-key
  anthropic_api_key: sk-ant-your-anthropic-key
  gemini_api_key: your-gemini-key
```

```bash
helm install choreoai choreoai/choreoai \
  --namespace choreoai \
  --create-namespace \
  --values values-production.yaml \
  --values secrets.yaml
```

### Override Nested Values

```bash
# Override nested values
helm install choreoai choreoai/choreoai \
  --set image.repository=myregistry/choreoai \
  --set image.tag=custom \
  --set autoscaling.maxReplicas=20 \
  --set ingress.hosts[0].host=api.example.com
```

### Values from Environment

```bash
# Use environment variables
export OPENAI_KEY=sk-your-key
export ANTHROPIC_KEY=sk-ant-your-key

helm install choreoai choreoai/choreoai \
  --set secrets.openai_api_key=$OPENAI_KEY \
  --set secrets.anthropic_api_key=$ANTHROPIC_KEY
```

## Hooks and Tests

### Pre-install Hook

```yaml
# templates/pre-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ .Release.Name }}-pre-install"
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      containers:
      - name: pre-install
        image: busybox
        command: ['sh', '-c', 'echo Pre-install tasks']
      restartPolicy: Never
```

### Test Hook

```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ .Release.Name }}-test-connection"
  annotations:
    "helm.sh/hook": test
spec:
  containers:
  - name: wget
    image: busybox
    command: ['wget']
    args: ['{{ include "choreoai.fullname" . }}:{{ .Values.service.port }}/health']
  restartPolicy: Never
```

### Run Tests

```bash
# Run Helm tests
helm test choreoai -n choreoai
```

## Chart Development

### Create New Chart

```bash
# Create chart scaffold
helm create mychart

# Lint chart
helm lint ./choreoai

# Package chart
helm package ./choreoai

# Generate documentation
helm-docs
```

### Template Functions

```yaml
# templates/_helpers.tpl
{{- define "choreoai.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "choreoai.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
```

### Values Schema Validation

```json
{
  "$schema": "http://json-schema.org/schema#",
  "type": "object",
  "required": ["replicaCount", "image"],
  "properties": {
    "replicaCount": {
      "type": "integer",
      "minimum": 1
    },
    "image": {
      "type": "object",
      "required": ["repository", "tag"],
      "properties": {
        "repository": {
          "type": "string"
        },
        "tag": {
          "type": "string"
        }
      }
    }
  }
}
```

## Best Practices

### 1. Pin Chart Versions

```bash
# Good - specific version
helm install choreoai choreoai/choreoai --version 1.2.3

# Bad - latest version
helm install choreoai choreoai/choreoai
```

### 2. Use Values Files

```bash
# Good - values in file
helm install choreoai choreoai/choreoai -f values-prod.yaml

# Bad - inline values (hard to maintain)
helm install choreoai choreoai/choreoai --set key1=val1 --set key2=val2
```

### 3. Separate Secrets

```bash
# Keep secrets in separate file
helm install choreoai choreoai/choreoai \
  -f values-prod.yaml \
  -f secrets.yaml  # Not committed to git
```

### 4. Use Dry Run

```bash
# Always test before applying
helm install choreoai choreoai/choreoai \
  -f values-prod.yaml \
  --dry-run --debug
```

### 5. Enable Atomic Upgrades

```bash
# Rollback on failure
helm upgrade choreoai choreoai/choreoai \
  --atomic \
  --timeout 10m
```

### 6. Document Values

```yaml
# values.yaml with comments
# Number of replicas to deploy
replicaCount: 3

# Image configuration
image:
  # Image repository
  repository: choreoai/choreoai
  # Image tag
  tag: "v1.2.3"
```

### 7. Use NOTES.txt

```
# templates/NOTES.txt
Thank you for installing {{ .Chart.Name }}.

Your release is named {{ .Release.Name }}.

To access your application:

  kubectl port-forward svc/{{ include "choreoai.fullname" . }} 8000:80 -n {{ .Release.Namespace }}

Then visit http://localhost:8000
```

## Troubleshooting

### Chart Installation Fails

**Check syntax:**
```bash
helm lint ./choreoai
```

**Debug template rendering:**
```bash
helm template choreoai ./choreoai --debug
```

**View generated manifests:**
```bash
helm get manifest choreoai -n choreoai
```

### Values Not Applied

**Check current values:**
```bash
helm get values choreoai -n choreoai
```

**Check all values (including defaults):**
```bash
helm get values choreoai -n choreoai --all
```

### Release Stuck

**Check release status:**
```bash
helm status choreoai -n choreoai
```

**Force delete:**
```bash
helm uninstall choreoai -n choreoai --no-hooks
```

### Hook Failures

**View hook logs:**
```bash
kubectl logs -l "helm.sh/hook" -n choreoai
```

**Delete failed hooks:**
```bash
kubectl delete jobs -l "helm.sh/hook" -n choreoai
```

### Upgrade Fails

**Check diff:**
```bash
# Install helm-diff plugin
helm plugin install https://github.com/databus23/helm-diff

# View differences
helm diff upgrade choreoai choreoai/choreoai \
  -f values-prod.yaml
```

**Rollback:**
```bash
helm rollback choreoai -n choreoai
```

### Chart Not Found

**Update repositories:**
```bash
helm repo update
```

**Check repository:**
```bash
helm repo list
helm search repo choreoai
```

## Next Steps

1. **Configuration**: Review [Configuration Reference](configuration.md) for all options
2. **Monitoring**: Set up [Monitoring](monitoring.md) for production
3. **Security**: Implement security best practices
4. **CI/CD**: Integrate with your deployment pipeline
5. **GitOps**: Consider ArgoCD or Flux for declarative deployments

## Additional Resources

- [Helm Official Documentation](https://helm.sh/docs/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Chart Template Guide](https://helm.sh/docs/chart_template_guide/)
- [ChoreoAI GitHub Repository](https://github.com/choreoai/choreoai)
