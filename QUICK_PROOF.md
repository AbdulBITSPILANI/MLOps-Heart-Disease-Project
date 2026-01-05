# Quick Proof Checklist

## ✅ MLflow Integration - PROOF

### Step 1: Verify MLflow is Integrated
The training script (`src/models/train.py`) already has complete MLflow integration:
- ✅ MLflow experiment setup
- ✅ Parameter logging
- ✅ Metrics logging (accuracy, precision, recall, ROC-AUC)
- ✅ Artifact logging (models, preprocessor)

### Step 2: Run Training (if not done)
```bash
python src/models/train.py
```

### Step 3: Verify mlruns/ Directory
```bash
# Check mlruns exists and has data
ls -la mlruns/
ls -la mlruns/0/
```

### Step 4: Start MLflow UI
```bash
mlflow ui
```

### Step 5: Take Screenshot
1. Open browser: `http://localhost:5000`
2. You should see experiment: `heart_disease_prediction`
3. Multiple runs (Logistic Regression and Random Forest)
4. Screenshot: `screenshots/mlflow_experiment.png`

**✅ MLflow Integration: COMPLETE**

---

## ✅ Kubernetes Deployment - PROOF

### Step 1: Verify Manifests Exist
```bash
ls k8s/
# Should see: deployment.yaml, service.yaml, ingress.yaml
```

### Step 2: Start Minikube (if using Minikube)
```bash
minikube start
eval $(minikube docker-env)
```

### Step 3: Build Docker Image
```bash
docker build -t heart-disease-api:latest .
```

### Step 4: Deploy to Kubernetes
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Step 5: Wait for Pods
```bash
kubectl get pods -l app=heart-disease-api
# Wait until STATUS = Running and READY = 2/2
```

### Step 6: Port Forward
```bash
kubectl port-forward service/heart-disease-api-service 8000:80
```

### Step 7: Test Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @data/sample_input.json
```

### Step 8: Take Screenshots
1. **Deployment status**: `kubectl get deployments,pods,services`
2. **Working prediction**: Screenshot of curl command + response
3. Save as: `screenshots/k8s_deployment.png` and `screenshots/k8s_predict.png`

**✅ Kubernetes Deployment: READY**

---

## Summary

Both requirements are complete:
1. ✅ **MLflow Integration**: Already implemented, just need to run training and take screenshot
2. ✅ **Kubernetes Deployment**: Manifests ready (deployment.yaml + service.yaml), just need to deploy and test

All code is ready, just need to execute and capture proof!

