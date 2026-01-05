# Kubernetes Deployment Manifests

This directory contains Kubernetes deployment manifests for the Heart Disease Prediction API.

## Files

- `deployment.yaml`: Complete Kubernetes deployment configuration including:
  - Deployment with 2 replicas
  - Service (LoadBalancer type)
  - Ingress configuration

## Prerequisites

- Kubernetes cluster (GKE, EKS, AKS, or local like Minikube/Docker Desktop)
- kubectl configured and connected to your cluster
- Docker image built and available (either in registry or local)

## Deployment Steps

### 1. Build and Push Docker Image (if using remote registry)

```bash
# Build image
docker build -t heart-disease-api:latest .

# Tag for your registry (example: Docker Hub)
docker tag heart-disease-api:latest yourusername/heart-disease-api:latest

# Push to registry
docker push yourusername/heart-disease-api:latest
```

### 2. Update Image in deployment.yaml (if needed)

If using a remote registry, update the image name in `deployment.yaml`:
```yaml
image: yourusername/heart-disease-api:latest
```

For local deployments (Minikube/Docker Desktop), you may need to:
- Load image into cluster: `minikube image load heart-disease-api:latest`
- Or use `imagePullPolicy: Never` for local images

### 3. Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/deployment.yaml

# Or apply individually
kubectl apply -f k8s/
```

### 4. Check Deployment Status

```bash
# Check deployments
kubectl get deployments

# Check pods
kubectl get pods -l app=heart-disease-api

# Check services
kubectl get services

# Check ingress
kubectl get ingress
```

### 5. Access the Service

#### Using LoadBalancer (Cloud)
```bash
# Get external IP
kubectl get service heart-disease-api-service

# Access API
curl http://<EXTERNAL-IP>/health
```

#### Using Port Forward (Local/Testing)
```bash
# Port forward to service
kubectl port-forward service/heart-disease-api-service 8000:80

# Access API
curl http://localhost:8000/health
```

#### Using Ingress
```bash
# Get ingress address
kubectl get ingress

# Add to /etc/hosts (or Windows hosts file)
# <INGRESS-IP> heart-disease-api.local

# Access API
curl http://heart-disease-api.local/health
```

## Configuration Details

### Deployment
- **Replicas**: 2 (for high availability)
- **Resources**: 
  - Requests: 256Mi memory, 250m CPU
  - Limits: 512Mi memory, 500m CPU
- **Health Probes**:
  - Liveness: `/health` endpoint, 30s initial delay
  - Readiness: `/health` endpoint, 10s initial delay

### Service
- **Type**: LoadBalancer (for cloud deployments)
- **Port**: 80 (external) → 8000 (container)
- **Protocol**: TCP

### Ingress
- **Host**: heart-disease-api.local
- **Controller**: Nginx (default annotation)
- **Path**: / (root path)

## Scaling

### Manual Scaling
```bash
kubectl scale deployment heart-disease-api --replicas=3
```

### Auto-scaling (HPA)
Create `k8s/hpa.yaml`:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: heart-disease-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: heart-disease-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Apply:
```bash
kubectl apply -f k8s/hpa.yaml
```

## Monitoring

### View Logs
```bash
# All pods
kubectl logs -l app=heart-disease-api

# Specific pod
kubectl logs <pod-name>

# Follow logs
kubectl logs -f -l app=heart-disease-api
```

### Describe Resources
```bash
kubectl describe deployment heart-disease-api
kubectl describe service heart-disease-api-service
kubectl describe pod <pod-name>
```

### Metrics
Access Prometheus metrics:
```bash
# Port forward first
kubectl port-forward service/heart-disease-api-service 8000:80

# Access metrics
curl http://localhost:8000/metrics
```

## Updating Deployment

### Rolling Update
```bash
# Update image
kubectl set image deployment/heart-disease-api api=heart-disease-api:v2

# Check rollout status
kubectl rollout status deployment/heart-disease-api

# Rollback if needed
kubectl rollout undo deployment/heart-disease-api
```

### Apply Changes
```bash
# Edit deployment.yaml, then apply
kubectl apply -f k8s/deployment.yaml
```

## Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/deployment.yaml

# Or delete individually
kubectl delete deployment heart-disease-api
kubectl delete service heart-disease-api-service
kubectl delete ingress heart-disease-api-ingress
```

## Troubleshooting

### Pods not starting
```bash
# Check pod status
kubectl get pods -l app=heart-disease-api

# Describe pod for events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>
```

### Service not accessible
```bash
# Check service endpoints
kubectl get endpoints heart-disease-api-service

# Test from within cluster
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- curl http://heart-disease-api-service/health
```

### Image pull errors
- Verify image exists in registry
- Check imagePullSecrets if using private registry
- For local: use `imagePullPolicy: Never`

### Health check failures
- Verify `/health` endpoint works locally
- Check resource limits (may be too restrictive)
- Review liveness/readiness probe settings

## Production Considerations

1. **Secrets Management**: Use Kubernetes Secrets for sensitive data
2. **ConfigMaps**: Externalize configuration
3. **Resource Limits**: Adjust based on actual usage
4. **Network Policies**: Implement for security
5. **Ingress TLS**: Add SSL/TLS certificates
6. **Monitoring**: Integrate with Prometheus/Grafana
7. **Logging**: Centralized logging (ELK, Loki, etc.)
8. **Backup**: Regular backups of model files

