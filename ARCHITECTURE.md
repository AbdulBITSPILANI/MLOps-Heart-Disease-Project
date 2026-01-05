# Architecture Documentation

## System Architecture

### Overview
The Heart Disease Prediction system follows a modern MLOps architecture with clear separation of concerns and scalable deployment options.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                         │
│                   (API Consumers/Users)                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway/Load Balancer                │
│                    (Kubernetes Service)                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   FastAPI    │  │   FastAPI    │  │   FastAPI    │    │
│  │   Pod 1      │  │   Pod 2      │  │   Pod N      │    │
│  │  (Container) │  │  (Container) │  │  (Container) │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                           │                                 │
│                    ┌──────▼──────┐                          │
│                    │  Model &    │                          │
│                    │ Preprocessor│                          │
│                    │   (Loaded)  │                          │
│                    └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Monitoring Layer                         │
│  ┌──────────────┐  ┌──────────────┐                       │
│  │  Prometheus  │  │    Logging   │                       │
│  │   Metrics    │  │   (Stdout)   │                       │
│  └──────────────┘  └──────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Training Pipeline

1. **Data Acquisition**
   - Download from UCI repository
   - Store in `data/raw/`

2. **Data Processing**
   - Load and clean data
   - Handle missing values
   - Feature engineering

3. **Model Training**
   - Train multiple models (LR, RF)
   - Evaluate with cross-validation
   - Log experiments with MLflow

4. **Model Selection**
   - Compare metrics
   - Select best model
   - Save as production model

5. **Model Packaging**
   - Save model and preprocessor
   - Version with MLflow
   - Store in `models/`

### Inference Pipeline

1. **Request Reception**
   - FastAPI receives HTTP POST request
   - Validates input schema (Pydantic)

2. **Preprocessing**
   - Load preprocessor
   - Transform input features
   - Handle missing values, scaling

3. **Prediction**
   - Load production model
   - Generate prediction and probability
   - Determine confidence level

4. **Response**
   - Format response (JSON)
   - Log request/metrics
   - Return to client

## Deployment Architecture

### Local Development
```
Developer Machine
├── Python Virtual Environment
├── Local API Server (uvicorn)
├── Local Model Files
└── Local Data
```

### Docker Deployment
```
Docker Container
├── Python 3.9 Runtime
├── Application Code
├── Dependencies (requirements.txt)
├── Model Files (mounted/copied)
└── API Server (uvicorn)
```

### Kubernetes Deployment
```
Kubernetes Cluster
├── Deployment (2+ replicas)
│   ├── Pod 1 (Container)
│   ├── Pod 2 (Container)
│   └── Pod N (Container)
├── Service (LoadBalancer)
├── Ingress (Optional)
└── ConfigMap/Secrets (if needed)
```

## Technology Stack

### Core Technologies
- **Python 3.9**: Programming language
- **FastAPI**: Web framework
- **Scikit-learn**: Machine learning
- **MLflow**: Experiment tracking
- **Docker**: Containerization
- **Kubernetes**: Orchestration

### Libraries & Tools
- **Pandas/NumPy**: Data processing
- **Matplotlib/Seaborn**: Visualization
- **Pytest**: Testing
- **Prometheus**: Metrics
- **Uvicorn**: ASGI server

## Security Considerations

1. **Input Validation**: Pydantic models validate all inputs
2. **Error Handling**: Proper exception handling and logging
3. **Resource Limits**: Kubernetes resource constraints
4. **Health Checks**: Liveness and readiness probes
5. **Logging**: Structured logging for audit trails

## Scalability

1. **Horizontal Scaling**: Kubernetes replicas
2. **Load Balancing**: Service layer distribution
3. **Resource Management**: CPU/Memory limits
4. **Stateless Design**: No session state in API

## Monitoring & Observability

1. **Metrics**: Prometheus metrics endpoint
2. **Logging**: Structured application logs
3. **Health Checks**: `/health` endpoint
4. **Request Tracking**: Request/response logging

## Future Enhancements

1. **Model Registry**: Centralized model storage
2. **A/B Testing**: Multiple model versions
3. **Auto-scaling**: HPA based on metrics
4. **Caching**: Redis for predictions
5. **API Gateway**: Rate limiting, authentication


