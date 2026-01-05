"""
FastAPI Application for Heart Disease Prediction API
Includes monitoring, logging, and metrics endpoints
"""

from src.utils.preprocessing import HeartDiseasePreprocessor
import logging
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import sys
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time


# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Heart Disease Prediction API",
    description="MLOps API for predicting heart disease risk",
)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total number of API requests",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    "api_request_duration_seconds",
    "API request duration in seconds",
    ["method", "endpoint"],
)

PREDICTION_COUNT = Counter(
    "predictions_total", "Total number of predictions", ["prediction_class"]
)

# Load model and preprocessor
MODEL_PATH = Path("models/production_model.pkl")
PREPROCESSOR_PATH = Path("models/preprocessor.pkl")

model = None
preprocessor = None


def load_model():
    """Load the trained model and preprocessor"""
    global model, preprocessor

    try:
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
            logger.info(f"Model loaded from {MODEL_PATH}")
        else:
            logger.warning(f"Model not found at {MODEL_PATH}")

        if PREPROCESSOR_PATH.exists():
            preprocessor = HeartDiseasePreprocessor.load(PREPROCESSOR_PATH)
            logger.info(f"Preprocessor loaded from {PREPROCESSOR_PATH}")
        else:
            logger.warning(f"Preprocessor not found at {PREPROCESSOR_PATH}")

    except Exception as e:
        logger.error(f"Error loading model/preprocessor: {e}")


# Load model on startup
@app.on_event("startup")
async def startup_event():
    load_model()


# Pydantic models for request/response
class HeartDiseaseInput(BaseModel):
    """Input schema for prediction request"""

    age: float = Field(..., ge=0, le=120, description="Age in years")
    sex: int = Field(..., ge=0, le=1, description="Sex (0=female, 1=male)")
    cp: int = Field(..., ge=0, le=3, description="Chest pain type (0-3)")
    trestbps: float = Field(..., ge=0, description="Resting blood pressure")
    chol: float = Field(..., ge=0, description="Serum cholesterol in mg/dl")
    fbs: int = Field(
        ..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dl (0/1)"
    )
    restecg: int = Field(
        ..., ge=0, le=2, description="Resting electrocardiographic results (0-2)"
    )
    thalach: float = Field(..., ge=0, description="Maximum heart rate achieved")
    exang: int = Field(..., ge=0, le=1, description="Exercise induced angina (0/1)")
    oldpeak: float = Field(..., ge=0, description="ST depression induced by exercise")
    slope: int = Field(
        ..., ge=0, le=2, description="Slope of the peak exercise ST segment (0-2)"
    )
    ca: int = Field(..., ge=0, le=3, description="Number of major vessels (0-3)")
    thal: int = Field(..., ge=0, le=3, description="Thalassemia (0-3)")

    class Config:
        schema_extra = {
            "example": {
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
                "thal": 1,
            }
        }


class PredictionResponse(BaseModel):
    """Response schema for prediction"""

    prediction: int = Field(
        ..., description="Predicted class (0=No Disease, 1=Disease)"
    )
    probability: float = Field(..., description="Probability of disease (0-1)")
    confidence: str = Field(..., description="Confidence level")


# Middleware for logging and metrics
@app.middleware("http")
async def log_requests(request, call_next):
    """Middleware to log requests and track metrics"""
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    REQUEST_DURATION.labels(method=request.method, endpoint=request.url.path).observe(
        duration
    )

    REQUEST_COUNT.labels(
        method=request.method, endpoint=request.url.path, status=response.status_code
    ).inc()

    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {duration:.4f}s"
    )

    return response


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    REQUEST_COUNT.labels(method="GET", endpoint="/", status=200).inc()
    return {"message": "Heart Disease Prediction API", "status": "operational"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "model_loaded": model is not None,
        "preprocessor_loaded": preprocessor is not None,
    }

    if not health_status["model_loaded"] or not health_status["preprocessor_loaded"]:
        health_status["status"] = "degraded"
        return JSONResponse(status_code=503, content=health_status)

    return health_status


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: HeartDiseaseInput):
    """
    Predict heart disease risk based on patient data

    Args:
        input_data: Patient health data

    Returns:
        Prediction result with probability and confidence
    """
    if model is None or preprocessor is None:
        logger.error("Model or preprocessor not loaded")
        raise HTTPException(
            status_code=503,
            detail="Model not available. Please check if model files are present.",
        )

    try:
        # Convert input to DataFrame
        input_dict = input_data.dict()
        input_df = pd.DataFrame([input_dict])

        # Ensure correct column order
        feature_order = [
            "age",
            "sex",
            "cp",
            "trestbps",
            "chol",
            "fbs",
            "restecg",
            "thalach",
            "exang",
            "oldpeak",
            "slope",
            "ca",
            "thal",
        ]
        input_df = input_df[feature_order]

        # Preprocess
        X_processed = preprocessor.transform(input_df)

        # Predict
        prediction = model.predict(X_processed)[0]
        probability = model.predict_proba(X_processed)[0][1]

        # Determine confidence level
        if probability < 0.3:
            confidence = "Low"
        elif probability < 0.7:
            confidence = "Medium"
        else:
            confidence = "High"

        # Log prediction
        logger.info(
            f"Prediction: {prediction}, "
            f"Probability: {probability:.4f}, "
            f"Confidence: {confidence}"
        )

        # Update metrics
        PREDICTION_COUNT.labels(prediction_class=str(prediction)).inc()

        return PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            confidence=confidence,
        )

    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
