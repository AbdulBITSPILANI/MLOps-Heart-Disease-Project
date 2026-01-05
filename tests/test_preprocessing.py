"""
Unit tests for preprocessing pipeline
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.utils.preprocessing import HeartDiseasePreprocessor, load_and_preprocess_data


class TestHeartDiseasePreprocessor:
    """Test cases for HeartDiseasePreprocessor"""
    
    def test_preprocessor_initialization(self):
        """Test preprocessor initialization"""
        preprocessor = HeartDiseasePreprocessor()
        assert preprocessor.scaler is not None
        assert preprocessor.imputer is not None
        assert preprocessor.is_fitted == False
    
    def test_fit_transform(self):
        """Test fit_transform method"""
        preprocessor = HeartDiseasePreprocessor()
        
        # Create sample data
        X = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50]
        })
        
        X_transformed = preprocessor.fit_transform(X)
        
        assert X_transformed.shape == X.shape
        assert preprocessor.is_fitted == True
        assert preprocessor.feature_names == ['feature1', 'feature2']
    
    def test_transform_without_fit(self):
        """Test that transform raises error if not fitted"""
        preprocessor = HeartDiseasePreprocessor()
        X = pd.DataFrame({'feature1': [1, 2, 3]})
        
        with pytest.raises(ValueError, match="must be fitted"):
            preprocessor.transform(X)
    
    def test_fit_transform_then_transform(self):
        """Test fit_transform followed by transform"""
        preprocessor = HeartDiseasePreprocessor()
        
        X_train = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50]
        })
        
        X_test = pd.DataFrame({
            'feature1': [6, 7],
            'feature2': [60, 70]
        })
        
        # Fit on training data
        X_train_transformed = preprocessor.fit_transform(X_train)
        
        # Transform test data
        X_test_transformed = preprocessor.transform(X_test)
        
        assert X_train_transformed.shape[1] == X_test_transformed.shape[1]
        assert X_test_transformed.shape[0] == 2
    
    def test_save_and_load(self, tmp_path):
        """Test saving and loading preprocessor"""
        preprocessor = HeartDiseasePreprocessor()
        
        X = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50]
        })
        
        preprocessor.fit_transform(X)
        
        # Save
        filepath = tmp_path / "preprocessor.pkl"
        preprocessor.save(filepath)
        
        # Load
        loaded_preprocessor = HeartDiseasePreprocessor.load(filepath)
        
        assert loaded_preprocessor.is_fitted == True
        assert loaded_preprocessor.feature_names == preprocessor.feature_names
        
        # Test that loaded preprocessor works
        X_test = pd.DataFrame({
            'feature1': [6, 7],
            'feature2': [60, 70]
        })
        transformed = loaded_preprocessor.transform(X_test)
        assert transformed.shape == (2, 2)
    
    def test_handles_missing_values(self):
        """Test that preprocessor handles missing values"""
        preprocessor = HeartDiseasePreprocessor()
        
        X = pd.DataFrame({
            'feature1': [1, 2, np.nan, 4, 5],
            'feature2': [10, 20, 30, np.nan, 50]
        })
        
        X_transformed = preprocessor.fit_transform(X)
        
        # Check no NaN values in output
        assert X_transformed.isna().sum().sum() == 0


class TestLoadAndPreprocessData:
    """Test cases for load_and_preprocess_data function"""
    
    def test_load_data_structure(self, tmp_path):
        """Test data loading returns correct structure"""
        # Create sample data file
        data_file = tmp_path / "test_data.csv"
        
        sample_data = pd.DataFrame({
            'age': [63, 67],
            'sex': [1, 1],
            'cp': [3, 2],
            'trestbps': [145, 160],
            'chol': [233, 286],
            'fbs': [1, 0],
            'restecg': [0, 0],
            'thalach': [150, 108],
            'exang': [0, 1],
            'oldpeak': [2.3, 1.5],
            'slope': [0, 2],
            'ca': [0, 3],
            'thal': [1, 2],
            'target': [1, 0]
        })
        
        sample_data.to_csv(data_file, index=False)
        
        X, y = load_and_preprocess_data(str(data_file))
        
        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)
        assert len(X) == len(y)
        assert 'target' not in X.columns
        assert y.isin([0, 1]).all()  # Binary target


