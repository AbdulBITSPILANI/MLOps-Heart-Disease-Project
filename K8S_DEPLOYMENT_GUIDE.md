# Kubernetes Deployment Guide

## ✅ Deployment Manifests Ready

All Kubernetes manifests are ready for deployment:
- `k8s/deployment.yaml` - Deployment configuration
- `k8s/service.yaml` - Service configuration  
- `k8s/ingress.yaml` - Ingress configuration (optional)

## Quick Deployment on Minikube/Docker Desktop

### Prerequisites
1. Minikube installed OR Docker Desktop with Kubernetes enabled
2. kubectl configured
3. Docker image built

### Step 1: Start Minikube (if using Minikube)
```bash
minikube start
```

### Step 2: Build Docker Image

**For Minikube:**
```bash
# Set Docker environment to Minikube
eval $(minikube docker-env)

# Build image
docker build -t heart-disease-api:latest .

# Verify image
docker images | grep heart-disease-api
```

**For Docker Desktop:**
```bash
# Build image
docker build -t heart-disease-api:latest .

# Or use existing image if already built
```

### Step 3: Update Image Pull Policy (if using local image)

Edit `k8s/deployment.yaml` and set:
```yaml
imagePullPolicy: Never  # For local images
```

Or leave as `IfNotPresent` if image is in registry.

### Step 4: Deploy to Kubernetes
```bash
# Apply all manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Or apply all at once
kubectl apply -f k8s/
```

### Step 5: Check Deployment Status
```bash
# Check deployments
kubectl get deployments

# Check pods (wait until READY 2/2)
kubectl get pods -l app=heart-disease-api

# Check services
kubectl get services

# Watch pod status
kubectl get pods -l app=heart-disease-api -w
```

### Step 6: Access the Service

**Option A: Port Forward (Easiest for Testing)**
```bash
# Port forward to service
kubectl port-forward service/heart-disease-api-service 8000:80

# Test in another terminal
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @data/sample_input.json
```

**Option B: Minikube Service (Minikube only)**
```bash
# Get service URL
minikube service heart-disease-api-service --url

# Use the returned URL
curl http://<URL>/health
```

**Option C: NodePort/LoadBalancer (Cloud/Minikube)**
```bash
# For Minikube, use tunnel
minikube tunnel

# Get external IP
kubectl get service heart-disease-api-service

# Access via external IP
curl http://<EXTERNAL-IP>/health
```

### Step 7: Test Prediction Endpoint

```bash
# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63,
    "sex": 1,
    "cp": 3,
    "trestbps": 145,
    "chol": 233,
    "fbs": 1,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 2.3,
    "slope": 0,
    "ca": 0,
    "thal": 1
  }'
```

Expected response:
```json
{
  "prediction": 0,
  "probability": 0.19,
  "confidence": "Low"
}
```

## Screenshot Checklist

Take screenshots of:

1. **Deployment Status**:
   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl get services
   ```

2. **Working Prediction**:
   - Screenshot of `/predict` endpoint response
   - Show both the curl command and response

3. **Pod Logs** (optional):
   ```bash
   kubectl logs -l app=heart-disease-api --tail=20
   ```

Save screenshots as:
- `screenshots/k8s_deployment_status.png`
- `screenshots/k8s_predict_working.png`
- `screenshots/k8s_pods_running.png`

## Troubleshooting

### Pods not starting
```bash
# Check pod status
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Common issues:
# - Image not found -> Build image or set imagePullPolicy: Never
# - CrashLoopBackOff -> Check logs for errors
# - ImagePullBackOff -> Check image name and registry
```

### Service not accessible
```bash
# Check service endpoints
kubectl get endpoints heart-disease-api-service

# Test from within cluster
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://heart-disease-api-service/health
```

### Health check failures
```bash
# Check if health endpoint works in pod
kubectl exec <pod-name> -- curl localhost:8000/health

# Adjust probe settings in deployment.yaml if needed
```

## Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/

# Or delete individually
kubectl delete deployment heart-disease-api
kubectl delete service heart-disease-api-service
kubectl delete ingress heart-disease-api-ingress
```

## Quick Verification Script

```bash
#!/bin/bash
echo "Checking Kubernetes deployment..."

echo "1. Deployments:"
kubectl get deployments

echo -e "\n2. Pods:"
kubectl get pods -l app=heart-disease-api

echo -e "\n3. Services:"
kubectl get services

echo -e "\n4. Testing /health endpoint:"
kubectl port-forward service/heart-disease-api-service 8000:80 &
sleep 3
curl http://localhost:8000/health
pkill -f port-forward
```

## Deployment Status: ✅ READY

All manifests are ready. Just deploy and test!

