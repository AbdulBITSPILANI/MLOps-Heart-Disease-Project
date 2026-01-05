# Quick Start Guide

## Prerequisites

- Python 3.9+
- Docker (optional, for containerization)
- Git

## Installation

### Option 1: Using pip (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd MLOPS_Project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using conda

```bash
# Clone the repository
git clone <repository-url>
cd MLOPS_Project

# Create conda environment
conda env create -f environment.yml
conda activate mlops-project
```

## Running the Pipeline

### Step 1: Download Data

```bash
python src/data/download_data.py
```

### Step 2: Explore Data (Optional)

```bash
jupyter notebook notebooks/eda.ipynb
```

### Step 3: Train Models

```bash
python src/models/train.py
```

This will:
- Load and preprocess data
- Train Logistic Regression and Random Forest models
- Evaluate models with cross-validation
- Save the best model to `models/production_model.pkl`
- Log experiments to MLflow

### Step 4: Start API Server

```bash
python src/api/main.py
```

Or using uvicorn:

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Step 5: Test the API

**Easiest Method - Interactive Docs:**
1. Open browser: `http://localhost:8000/docs`
2. Find `/predict` endpoint
3. Click "Try it out"
4. Edit the JSON input
5. Click "Execute"

**Using test scripts:**
```bash
# Quick test with sample data
python scripts/test_api.py

# Custom input test
python test_prediction.py
```

**Using curl:**
```bash
curl -X POST "http://localhost:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d @data/sample_input.json
```

See `HOW_TO_USE_API.md` for detailed examples and input field descriptions.

## Docker Deployment

### Build Image

```bash
docker build -t heart-disease-api .
```

### Run Container

```bash
docker run -p 8000:8000 heart-disease-api
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (or Docker Desktop with Kubernetes enabled)
- kubectl configured

### Deploy

```bash
kubectl apply -f k8s/deployment.yaml
```

### Check Status

```bash
kubectl get deployments
kubectl get services
kubectl get pods
```

### Access Service

```bash
# Get service URL
kubectl get service heart-disease-api-service

# Or use port-forward for local testing
kubectl port-forward service/heart-disease-api-service 8000:80
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

## API Documentation

Once the API is running, visit:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`
- Metrics: `http://localhost:8000/metrics`

## Common Issues

### Model Not Found Error

If you see "Model not available" error:
1. Make sure you've trained the model: `python src/models/train.py`
2. Check that `models/production_model.pkl` exists
3. Check that `models/preprocessor.pkl` exists

### Port Already in Use

If port 8000 is already in use:
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8001
```

### Docker Build Fails

Make sure:
- Docker is running
- You're in the project root directory
- All dependencies are listed in requirements.txt

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system architecture
- Review [REPORT.md](REPORT.md) for project report
- Explore the notebooks for data analysis


