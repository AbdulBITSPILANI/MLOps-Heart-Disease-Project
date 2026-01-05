# API Access Guide

## Important: URL vs Bind Address

When you run the API with:
```bash
python src/api/main.py
```

The API **binds to** `0.0.0.0:8000` (listens on all network interfaces), but you **access it via**:
- ✅ `http://localhost:8000`
- ✅ `http://127.0.0.1:8000`

❌ **Do NOT use**: `http://0.0.0.0:8000` (this won't work in browsers/curl)

## Quick Start

1. **Start the API** (in one terminal):
   ```bash
   python src/api/main.py
   ```
   
   Or use the helper script:
   ```bash
   # Windows
   .\run_api.bat
   
   # Linux/Mac
   ./run_api.sh
   ```

2. **Access the API**:
   - Open in browser: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

3. **Test the API** (in another terminal):
   ```bash
   python scripts/test_api.py
   ```

## Available Endpoints

- **GET /** - API information
- **GET /health** - Health check with model status
- **GET /metrics** - Prometheus metrics
- **GET /docs** - Interactive API documentation (Swagger UI)
- **GET /redoc** - Alternative API documentation
- **POST /predict** - Make predictions

## Example Requests

### Using curl:
```bash
# Health check
curl http://localhost:8000/health

# Prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d @data/sample_input.json
```

### Using Python:
```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())

# Prediction
data = {
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
}

response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
```

## Troubleshooting

### "Cannot be reached" error
- ✅ Make sure you're using `http://localhost:8000` (not `0.0.0.0:8000`)
- ✅ Check that the API server is running (look for "Application startup complete" message)
- ✅ Try `http://127.0.0.1:8000` instead

### Port already in use
If port 8000 is already in use:
```bash
# Kill the process using port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or run on a different port
uvicorn src.api.main:app --host 0.0.0.0 --port 8001
```

### Model not found
Make sure you've trained the models first:
```bash
python src/models/train.py
```

This will create:
- `models/production_model.pkl`
- `models/preprocessor.pkl`

