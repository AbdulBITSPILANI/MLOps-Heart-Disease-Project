"""
Unit tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys
import joblib
import pandas as pd
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from src.api.main import app
from src.utils.preprocessing import HeartDiseasePreprocessor
from sklearn.linear_model import LogisticRegression


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def sample_model_and_preprocessor(tmp_path):
    """Create sample model and preprocessor for testing"""
    # Create directories
    models_dir = tmp_path / "models"
    models_dir.mkdir()

    # Create sample data
    X = np.random.randn(100, 13)
    y = np.random.randint(0, 2, 100)

    # Create and fit preprocessor
    preprocessor = HeartDiseasePreprocessor()
    X_processed = preprocessor.fit_transform(pd.DataFrame(X))

    # Create and fit model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_processed, y)

    # Save
    model_path = models_dir / "production_model.pkl"
    preprocessor_path = models_dir / "preprocessor.pkl"

    joblib.dump(model, model_path)
    preprocessor.save(preprocessor_path)

    return model_path, preprocessor_path


class TestAPIEndpoints:
    """Test cases for API endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["status"] == "operational"

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code in [200, 503]  # May be 503 if model not loaded
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data

    def test_metrics_endpoint(self, client):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]

    def test_predict_endpoint_valid_input(
        self, client, sample_model_and_preprocessor, monkeypatch
    ):
        """Test predict endpoint with valid input"""
        model_path, preprocessor_path = sample_model_and_preprocessor

        # Mock model paths
        import src.api.main as api_module

        original_model_path = api_module.MODEL_PATH
        original_preprocessor_path = api_module.PREPROCESSOR_PATH

        monkeypatch.setattr(api_module, "MODEL_PATH", model_path)
        monkeypatch.setattr(api_module, "PREPROCESSOR_PATH", preprocessor_path)

        # Reload model
        api_module.load_model()

        # Valid input
        input_data = {
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

        response = client.post("/predict", json=input_data)

        # Restore original paths
        monkeypatch.setattr(api_module, "MODEL_PATH", original_model_path)
        monkeypatch.setattr(api_module, "PREPROCESSOR_PATH", original_preprocessor_path)

        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "probability" in data
        assert "confidence" in data
        assert data["prediction"] in [0, 1]
        assert 0 <= data["probability"] <= 1

    def test_predict_endpoint_invalid_input(self, client):
        """Test predict endpoint with invalid input"""
        # Missing required field
        invalid_data = {
            "age": 63,
            "sex": 1,
            # Missing other fields
        }

        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422  # Validation error

    def test_predict_endpoint_out_of_range(self, client):
        """Test predict endpoint with out of range values"""
        invalid_data = {
            "age": 200,  # Out of range
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

        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422  # Validation error
