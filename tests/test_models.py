"""
Unit tests for model training and inference
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

sys.path.append(str(Path(__file__).parent.parent))

from src.utils.preprocessing import HeartDiseasePreprocessor


class TestModelTraining:
    """Test cases for model training"""

    def test_logistic_regression_training(self):
        """Test Logistic Regression can be trained"""
        # Create sample data
        X = np.random.randn(100, 13)
        y = np.random.randint(0, 2, 100)

        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X, y)

        predictions = model.predict(X)
        probabilities = model.predict_proba(X)

        assert len(predictions) == len(y)
        assert probabilities.shape == (100, 2)
        assert probabilities.sum(axis=1).all() == pytest.approx(1.0, abs=1e-6)

    def test_random_forest_training(self):
        """Test Random Forest can be trained"""
        X = np.random.randn(100, 13)
        y = np.random.randint(0, 2, 100)

        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)

        predictions = model.predict(X)
        probabilities = model.predict_proba(X)

        assert len(predictions) == len(y)
        assert probabilities.shape == (100, 2)

    def test_model_save_and_load(self, tmp_path):
        """Test model can be saved and loaded"""
        X = np.random.randn(50, 13)
        y = np.random.randint(0, 2, 50)

        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X, y)

        # Save
        model_path = tmp_path / "model.pkl"
        joblib.dump(model, model_path)

        # Load
        loaded_model = joblib.load(model_path)

        # Test predictions match
        original_pred = model.predict(X[:5])
        loaded_pred = loaded_model.predict(X[:5])

        np.testing.assert_array_equal(original_pred, loaded_pred)


class TestModelInference:
    """Test cases for model inference"""

    def test_preprocessor_model_integration(self):
        """Test preprocessor and model work together"""
        # Create sample data
        X_train = pd.DataFrame(np.random.randn(100, 13))
        y_train = np.random.randint(0, 2, 100)
        X_test = pd.DataFrame(np.random.randn(20, 13))

        # Preprocess
        preprocessor = HeartDiseasePreprocessor()
        X_train_processed = preprocessor.fit_transform(X_train)
        X_test_processed = preprocessor.transform(X_test)

        # Train model
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X_train_processed, y_train)

        # Predict
        predictions = model.predict(X_test_processed)
        probabilities = model.predict_proba(X_test_processed)

        assert len(predictions) == len(X_test)
        assert probabilities.shape == (20, 2)
        assert all(pred in [0, 1] for pred in predictions)
