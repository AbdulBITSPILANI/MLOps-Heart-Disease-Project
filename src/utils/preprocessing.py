"""
Preprocessing Pipeline for Heart Disease Dataset
Ensures reproducibility and consistency in data preprocessing
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from pathlib import Path
import joblib
import pickle


class HeartDiseasePreprocessor:
    """
    Preprocessing pipeline for heart disease dataset
    Handles missing values, encoding, and scaling
    """
    
    def __init__(self, scaler=None, imputer=None):
        """
        Initialize preprocessor
        
        Args:
            scaler: StandardScaler instance (optional, for inference)
            imputer: SimpleImputer instance (optional, for inference)
        """
        self.scaler = scaler if scaler else StandardScaler()
        self.imputer = imputer if imputer else SimpleImputer(strategy='median')
        self.feature_names = None
        self.is_fitted = False
        
    def fit_transform(self, X):
        """
        Fit preprocessor on training data and transform
        
        Args:
            X: Input features (DataFrame or array)
            
        Returns:
            Transformed features
        """
        # Convert to DataFrame if numpy array
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
            
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Handle missing values
        X_imputed = self.imputer.fit_transform(X)
        X_imputed = pd.DataFrame(X_imputed, columns=self.feature_names)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_imputed)
        X_scaled = pd.DataFrame(X_scaled, columns=self.feature_names)
        
        self.is_fitted = True
        
        return X_scaled
    
    def transform(self, X):
        """
        Transform new data using fitted preprocessor
        
        Args:
            X: Input features (DataFrame or array)
            
        Returns:
            Transformed features
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
            
        # Convert to DataFrame if numpy array
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
            
        # Handle missing values
        X_imputed = self.imputer.transform(X)
        X_imputed = pd.DataFrame(X_imputed, columns=X.columns)
        
        # Scale features
        X_scaled = self.scaler.transform(X_imputed)
        X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
        
        return X_scaled
    
    def save(self, filepath):
        """Save preprocessor to disk"""
        preprocessor_data = {
            'scaler': self.scaler,
            'imputer': self.imputer,
            'feature_names': self.feature_names,
            'is_fitted': self.is_fitted
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(preprocessor_data, f)
    
    @classmethod
    def load(cls, filepath):
        """Load preprocessor from disk"""
        with open(filepath, 'rb') as f:
            preprocessor_data = pickle.load(f)
        
        preprocessor = cls(
            scaler=preprocessor_data['scaler'],
            imputer=preprocessor_data['imputer']
        )
        preprocessor.feature_names = preprocessor_data['feature_names']
        preprocessor.is_fitted = preprocessor_data['is_fitted']
        
        return preprocessor


def load_and_preprocess_data(data_path="data/raw/heart_disease_cleveland.csv"):
    """
    Load and preprocess heart disease dataset
    
    Args:
        data_path: Path to raw data file
        
    Returns:
        X: Features DataFrame
        y: Target Series
    """
    # Load data
    df = pd.read_csv(data_path)
    
    # Convert target to binary (0 = no disease, 1 = disease)
    # Original dataset: 0 = no disease, 1-4 = disease
    df['target'] = (df['target'] > 0).astype(int)
    
    # Separate features and target
    feature_columns = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ]
    
    X = df[feature_columns].copy()
    y = df['target'].copy()
    
    return X, y


