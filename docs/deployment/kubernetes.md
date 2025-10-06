# Kubernetes Deployment

Deploy ChoreoAI to Kubernetes for enterprise-grade orchestration, high availability, and automatic scaling.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Deployment Manifests](#deployment-manifests)
- [Configuration](#configuration)
- [Secrets Management](#secrets-management)
- [Networking](#networking)
- [Storage](#storage)
- [Auto-scaling](#auto-scaling)
- [High Availability](#high-availability)
- [Security](#security)
- [Monitoring](#monitoring)
- [Updates and Rollbacks](#updates-and-rollbacks)
- [Multi-cluster Deployment](#multi-cluster-deployment)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Kubernetes provides robust orchestration for ChoreoAI deployments with:

- Automatic scaling based on demand
- Self-healing and high availability
- Rolling updates with zero downtime
- Resource management and isolation
- Service discovery and load balancing

### When to Use Kubernetes

| Scenario | Recommended |
|----------|-------------|
| Production workloads | Yes |
| High availability requirements | Yes |
| Auto-scaling needed | Yes |
| Multi-region deployment | Yes |
| Development/testing | No (use Docker) |
| Simple single-node deployments | No (use Docker) |

## Prerequisites

### Required

- Kubernetes cluster 1.21+
- kubectl configured and authenticated
- At least one worker node with 2 CPU, 4GB RAM
- AI provider API keys

### Optional

- Helm 3.0+ (for simplified deployment)
- Ingress controller (nginx, traefik)
- Certificate manager (cert-manager)
- Monitoring stack (Prometheus, Grafana)

### Cluster Setup

**Local Development:**
```bash
# Minikube
minikube start --cpus=4 --memory=8192

# Kind
kind create cluster --config=kind-config.yaml

# K3s
curl -sfL https://get.k3s.io | sh -
```

**Cloud Providers:**
```bash
# AWS EKS
eksctl create cluster --name choreoai --nodes 3

# Google GKE
gcloud container clusters create choreoai --num-nodes=3

# Azure AKS
az aks create --name choreoai --node-count 3
```

**Verify cluster:**
```bash
kubectl cluster-info
kubectl get nodes
```

## Quick Start

### 1. Create Namespace

```bash
# Create dedicated namespace
kubectl create namespace choreoai

# Set as default
kubectl config set-context --current --namespace=choreoai
```

### 2. Create Secrets

```bash
# Create secret from literals
kubectl create secret generic choreoai-secrets \
  --from-literal=OPENAI_API_KEY=sk-your-key \
  --from-literal=ANTHROPIC_API_KEY=sk-ant-your-key \
  --from-literal=GEMINI_API_KEY=your-gemini-key \
  -n choreoai

# Or from file
kubectl create secret generic choreoai-secrets \
  --from-env-file=.env \
  -n choreoai
```

### 3. Deploy Application

```bash
# Apply all manifests
kubectl apply -f kubernetes/ -n choreoai

# Or individual components
kubectl apply -f deployment.yaml -n choreoai
kubectl apply -f service.yaml -n choreoai
kubectl apply -f ingress.yaml -n choreoai
```

### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n choreoai

# Check service
kubectl get svc -n choreoai

# Check deployment
kubectl get deployment -n choreoai

# View logs
kubectl logs -l app=choreoai -n choreoai
```

### 5. Test the API

```bash
# Port forward for local access
kubectl port-forward svc/choreoai 8000:80 -n choreoai

# Test health endpoint
curl http://localhost:8000/health

# Test chat completion
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Deployment Manifests

### Namespace

`namespace.yaml`:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: choreoai
  labels:
    name: choreoai
    environment: production
```

### Deployment

`deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: choreoai
  namespace: choreoai
  labels:
    app: choreoai
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: choreoai
  template:
    metadata:
      labels:
        app: choreoai
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: choreoai
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: choreoai
        image: choreoai/choreoai:v1.2.3
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        env:
        - name: PORT
          value: "8000"
        - name: HOST
          value: "0.0.0.0"
        - name: LOG_LEVEL
          value: "INFO"
        - name: ENVIRONMENT
          value: "production"
        envFrom:
        - secretRef:
            name: choreoai-secrets
        - configMapRef:
            name: choreoai-config
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/.cache
      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - choreoai
              topologyKey: kubernetes.io/hostname
```

### Service

`service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: choreoai
  namespace: choreoai
  labels:
    app: choreoai
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  type: ClusterIP
  selector:
    app: choreoai
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
  sessionAffinity: None
```

### ConfigMap

`configmap.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: choreoai-config
  namespace: choreoai
data:
  PORT: "8000"
  HOST: "0.0.0.0"
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  ALLOWED_ORIGINS: "*"
  AWS_REGION: "us-east-1"
```

### Ingress

`ingress.yaml`:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: choreoai
  namespace: choreoai
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - api.choreoai.example.com
    secretName: choreoai-tls
  rules:
  - host: api.choreoai.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: choreoai
            port:
              number: 80
```

### ServiceAccount

`serviceaccount.yaml`:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: choreoai
  namespace: choreoai
  labels:
    app: choreoai
```

## Configuration

### ConfigMap Management

```bash
# Create from file
kubectl create configmap choreoai-config \
  --from-file=config.yaml \
  -n choreoai

# Create from literal
kubectl create configmap choreoai-config \
  --from-literal=LOG_LEVEL=DEBUG \
  -n choreoai

# Update ConfigMap
kubectl edit configmap choreoai-config -n choreoai

# View ConfigMap
kubectl get configmap choreoai-config -o yaml -n choreoai
```

### Environment Variables

```yaml
env:
- name: PORT
  valueFrom:
    configMapKeyRef:
      name: choreoai-config
      key: PORT
- name: OPENAI_API_KEY
  valueFrom:
    secretKeyRef:
      name: choreoai-secrets
      key: OPENAI_API_KEY
```

## Secrets Management

### Native Kubernetes Secrets

```bash
# Create secret
kubectl create secret generic choreoai-secrets \
  --from-literal=OPENAI_API_KEY=sk-your-key \
  --from-literal=ANTHROPIC_API_KEY=sk-ant-your-key \
  -n choreoai

# Create from file
kubectl create secret generic choreoai-secrets \
  --from-env-file=.env \
  -n choreoai

# View secret (base64 encoded)
kubectl get secret choreoai-secrets -o yaml -n choreoai

# Decode secret
kubectl get secret choreoai-secrets \
  -o jsonpath='{.data.OPENAI_API_KEY}' \
  -n choreoai | base64 -d
```

### External Secrets Operator

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: choreoai-secrets
  namespace: choreoai
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: choreoai-secrets
    creationPolicy: Owner
  data:
  - secretKey: OPENAI_API_KEY
    remoteRef:
      key: choreoai/openai-key
  - secretKey: ANTHROPIC_API_KEY
    remoteRef:
      key: choreoai/anthropic-key
```

### Sealed Secrets

```bash
# Install sealed-secrets controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/controller.yaml

# Seal a secret
kubeseal --format yaml < secret.yaml > sealed-secret.yaml

# Apply sealed secret
kubectl apply -f sealed-secret.yaml -n choreoai
```

### HashiCorp Vault

```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: vault-choreoai
  namespace: choreoai
spec:
  provider: vault
  parameters:
    vaultAddress: "https://vault.example.com"
    roleName: "choreoai"
    objects: |
      - objectName: "OPENAI_API_KEY"
        secretPath: "secret/data/choreoai/openai"
        secretKey: "api_key"
```

## Networking

### Service Types

**ClusterIP (Default):**
```yaml
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000
```

**NodePort:**
```yaml
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 8000
    nodePort: 30080
```

**LoadBalancer:**
```yaml
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
```

### Network Policies

`networkpolicy.yaml`:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: choreoai-netpol
  namespace: choreoai
spec:
  podSelector:
    matchLabels:
      app: choreoai
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
  - to:
    - podSelector: {}
    ports:
    - protocol: TCP
      port: 443
```

### DNS Configuration

```yaml
spec:
  dnsPolicy: ClusterFirst
  dnsConfig:
    options:
    - name: ndots
      value: "2"
    - name: edns0
```

## Storage

### Persistent Volume Claims

`pvc.yaml`:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: choreoai-logs
  namespace: choreoai
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd
```

### Using PVC in Deployment

```yaml
spec:
  template:
    spec:
      volumes:
      - name: logs
        persistentVolumeClaim:
          claimName: choreoai-logs
      containers:
      - name: choreoai
        volumeMounts:
        - name: logs
          mountPath: /app/logs
```

### EmptyDir for Temporary Storage

```yaml
volumes:
- name: tmp
  emptyDir:
    medium: Memory
    sizeLimit: 1Gi
```

## Auto-scaling

### Horizontal Pod Autoscaler (HPA)

`hpa.yaml`:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: choreoai-hpa
  namespace: choreoai
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: choreoai
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

### Vertical Pod Autoscaler (VPA)

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: choreoai-vpa
  namespace: choreoai
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: choreoai
  updatePolicy:
    updateMode: Auto
  resourcePolicy:
    containerPolicies:
    - containerName: choreoai
      minAllowed:
        cpu: 500m
        memory: 1Gi
      maxAllowed:
        cpu: 4000m
        memory: 8Gi
```

### KEDA (Event-driven Autoscaling)

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: choreoai-scaledobject
  namespace: choreoai
spec:
  scaleTargetRef:
    name: choreoai
  minReplicaCount: 2
  maxReplicaCount: 20
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus:9090
      metricName: http_requests_per_second
      threshold: '100'
      query: sum(rate(http_requests_total[1m]))
```

## High Availability

### Pod Disruption Budget

`pdb.yaml`:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: choreoai-pdb
  namespace: choreoai
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: choreoai
```

### Multi-zone Deployment

```yaml
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - choreoai
        topologyKey: topology.kubernetes.io/zone
```

### Node Affinity

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: node.kubernetes.io/instance-type
            operator: In
            values:
            - m5.xlarge
            - m5.2xlarge
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - us-east-1a
```

## Security

### Pod Security Standards

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: choreoai
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Security Context

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: choreoai
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1000
      capabilities:
        drop:
        - ALL
```

### RBAC

`rbac.yaml`:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: choreoai-role
  namespace: choreoai
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: choreoai-rolebinding
  namespace: choreoai
subjects:
- kind: ServiceAccount
  name: choreoai
  namespace: choreoai
roleRef:
  kind: Role
  name: choreoai-role
  apiGroup: rbac.authorization.k8s.io
```

### Image Security

```yaml
spec:
  containers:
  - name: choreoai
    image: choreoai/choreoai:v1.2.3@sha256:abcdef...
    imagePullPolicy: Always
  imagePullSecrets:
  - name: registry-credentials
```

## Monitoring

### Prometheus ServiceMonitor

`servicemonitor.yaml`:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: choreoai
  namespace: choreoai
  labels:
    app: choreoai
spec:
  selector:
    matchLabels:
      app: choreoai
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### Metrics Server

```bash
# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# View resource usage
kubectl top pods -n choreoai
kubectl top nodes
```

See [Monitoring Guide](monitoring.md) for detailed setup.

## Updates and Rollbacks

### Rolling Update

```bash
# Update image
kubectl set image deployment/choreoai \
  choreoai=choreoai/choreoai:v1.3.0 \
  -n choreoai

# Watch rollout
kubectl rollout status deployment/choreoai -n choreoai

# View rollout history
kubectl rollout history deployment/choreoai -n choreoai
```

### Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/choreoai -n choreoai

# Rollback to specific revision
kubectl rollout undo deployment/choreoai \
  --to-revision=2 \
  -n choreoai
```

### Blue-Green Deployment

```bash
# Deploy green version
kubectl apply -f deployment-green.yaml

# Switch traffic
kubectl patch service choreoai \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Remove blue version
kubectl delete deployment choreoai-blue
```

### Canary Deployment

```yaml
# Primary deployment (90%)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: choreoai-primary
spec:
  replicas: 9
  template:
    metadata:
      labels:
        app: choreoai
        version: stable
---
# Canary deployment (10%)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: choreoai-canary
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: choreoai
        version: canary
```

## Multi-cluster Deployment

### Cluster Federation

```yaml
apiVersion: types.kubefed.io/v1beta1
kind: FederatedDeployment
metadata:
  name: choreoai
  namespace: choreoai
spec:
  template:
    spec:
      replicas: 3
  placement:
    clusters:
    - name: us-east-1
    - name: eu-west-1
  overrides:
  - clusterName: us-east-1
    clusterOverrides:
    - path: "/spec/replicas"
      value: 5
```

### Multi-region Strategy

```bash
# Deploy to multiple regions
for region in us-east-1 eu-west-1 ap-southeast-1; do
  kubectl --context=$region apply -f deployment.yaml
done
```

## Best Practices

### 1. Resource Requests and Limits

Always set appropriate resource requests and limits:

```yaml
resources:
  requests:
    cpu: 500m
    memory: 1Gi
  limits:
    cpu: 2000m
    memory: 4Gi
```

### 2. Health Checks

Configure both liveness and readiness probes:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
```

### 3. Labels and Annotations

Use consistent labeling:

```yaml
metadata:
  labels:
    app: choreoai
    version: v1.0.0
    environment: production
    component: api
```

### 4. Use Namespaces

Isolate resources using namespaces:

```bash
kubectl create namespace choreoai-prod
kubectl create namespace choreoai-staging
```

### 5. Pod Disruption Budgets

Ensure availability during updates:

```yaml
spec:
  minAvailable: 2
```

### 6. Network Policies

Restrict network access:

```yaml
spec:
  policyTypes:
  - Ingress
  - Egress
```

### 7. Security Contexts

Run as non-root with minimal privileges:

```yaml
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
```

### 8. Image Tags

Use specific version tags, not `latest`:

```yaml
image: choreoai/choreoai:v1.2.3
```

## Troubleshooting

### Pod Not Starting

**Check pod status:**
```bash
kubectl get pods -n choreoai
kubectl describe pod <pod-name> -n choreoai
```

**Common issues:**
- Image pull errors
- Resource constraints
- Missing secrets/configmaps
- Failed health checks

**Solutions:**
```bash
# Check events
kubectl get events -n choreoai --sort-by='.lastTimestamp'

# Check logs
kubectl logs <pod-name> -n choreoai

# Check previous container
kubectl logs <pod-name> -n choreoai --previous
```

### Service Not Accessible

**Check service:**
```bash
kubectl get svc -n choreoai
kubectl describe svc choreoai -n choreoai
```

**Test from within cluster:**
```bash
kubectl run -it --rm debug \
  --image=curlimages/curl \
  --restart=Never \
  -- curl http://choreoai.choreoai.svc.cluster.local/health
```

### High Resource Usage

**Check metrics:**
```bash
kubectl top pods -n choreoai
kubectl top nodes
```

**Solutions:**
- Adjust resource limits
- Scale horizontally
- Optimize application

### Persistent Volume Issues

**Check PVC status:**
```bash
kubectl get pvc -n choreoai
kubectl describe pvc <pvc-name> -n choreoai
```

**Check PV:**
```bash
kubectl get pv
kubectl describe pv <pv-name>
```

### Network Issues

**Test DNS:**
```bash
kubectl run -it --rm debug \
  --image=busybox \
  --restart=Never \
  -- nslookup choreoai.choreoai.svc.cluster.local
```

**Check network policies:**
```bash
kubectl get networkpolicies -n choreoai
```

### ImagePullBackOff

**Check image pull secret:**
```bash
kubectl get secret registry-credentials -n choreoai

# Create if missing
kubectl create secret docker-registry registry-credentials \
  --docker-server=registry.example.com \
  --docker-username=user \
  --docker-password=pass \
  -n choreoai
```

## Next Steps

1. **Simplified Deployment**: Use [Helm](helm.md) for easier management
2. **Configuration**: Review [Configuration Reference](configuration.md)
3. **Monitoring**: Set up [Monitoring](monitoring.md) stack
4. **Security**: Implement security best practices
5. **Optimization**: Fine-tune resource allocation

## Additional Resources

- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Production Best Practices](https://kubernetes.io/docs/setup/best-practices/)
- [ChoreoAI GitHub Repository](https://github.com/choreoai/choreoai)
