# MLOps Project: Heart Disease Prediction

End-to-End ML Model Development, CI/CD, and Production Deployment

## Project Overview

This project implements a complete MLOps pipeline for predicting heart disease risk using patient health data. The solution includes data acquisition, EDA, model development, experiment tracking, containerization, CI/CD, and cloud deployment.

## Dataset

- **Title**: Heart Disease UCI Dataset
- **Source**: UCI Machine Learning Repository
- **Features**: 14+ features (age, sex, blood pressure, cholesterol, etc.)
- **Target**: Binary classification (presence/absence of heart disease)

## Project Structure

```
MLOPS_Project/
├── data/
│   ├── raw/                 # Raw dataset
│   └── processed/           # Processed data
├── src/
│   ├── data/                # Data processing scripts
│   ├── models/              # Model training scripts
│   ├── api/                 # API server code
│   └── utils/               # Utility functions
├── notebooks/
│   └── eda.ipynb            # Exploratory Data Analysis
├── tests/                   # Unit tests
├── models/                  # Saved models
├── mlruns/                  # MLflow tracking data
├── k8s/                     # Kubernetes manifests
├── .github/
│   └── workflows/           # GitHub Actions CI/CD
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Docker (for containerization)
- Kubernetes cluster (for deployment) or Docker Desktop
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd MLOPS_Project
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the dataset:
```bash
python src/data/download_data.py
```

## Usage

### 1. Exploratory Data Analysis

Run the EDA notebook:
```bash
jupyter notebook notebooks/eda.ipynb
```

### 2. Model Training

Train models with MLflow tracking:
```bash
python src/models/train.py
```

### 3. Run API Locally

Start the FastAPI server:
```bash
python src/api/main.py
```

Or using uvicorn:
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

**Note:** The API binds to `0.0.0.0:8000`, but you access it via `http://localhost:8000` or `http://127.0.0.1:8000`

### 4. Docker Deployment

Build the Docker image:
```bash
docker build -t heart-disease-api .
```

Run the container:
```bash
docker run -p 8000:8000 heart-disease-api
```

### 5. Kubernetes Deployment

Deploy to Kubernetes:
```bash
kubectl apply -f k8s/
```

## API Endpoints

- `GET /`: Health check
- `GET /health`: Health check with metrics
- `POST /predict`: Predict heart disease risk

### Example Prediction Request

```bash
curl -X POST "http://localhost:8000/predict" \
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

## Testing

Run unit tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## CI/CD

The project uses GitHub Actions for CI/CD. The workflow includes:
- Code linting (flake8, black)
- Unit testing
- Model training validation
- Docker build verification

Workflow file: `.github/workflows/ci_cd.yml`

## Monitoring

The API includes:
- Request logging
- Prometheus metrics endpoint (`/metrics`)
- Health check endpoint

## License

MIT License

## Author

MLOps Experimental Learning Assignment


