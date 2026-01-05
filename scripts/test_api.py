"""
Script to test the API endpoints
"""

import requests
import json
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_predict():
    """Test predict endpoint"""
    print("Testing /predict endpoint...")
    
    # Load sample input
    sample_input_path = Path("data/sample_input.json")
    if sample_input_path.exists():
        with open(sample_input_path, 'r') as f:
            input_data = json.load(f)
    else:
        # Default sample data
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
            "thal": 1
        }
    
    response = requests.post(f"{BASE_URL}/predict", json=input_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_metrics():
    """Test metrics endpoint"""
    print("Testing /metrics endpoint...")
    response = requests.get(f"{BASE_URL}/metrics")
    print(f"Status Code: {response.status_code}")
    print(f"Response (first 500 chars): {response.text[:500]}")
    print()

if __name__ == "__main__":
    try:
        # Test root endpoint
        print("=" * 50)
        print("Testing API Endpoints")
        print("=" * 50)
        print()
        
        response = requests.get(f"{BASE_URL}/")
        print("Testing / endpoint...")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        
        test_health()
        test_metrics()
        test_predict()
        
        print("=" * 50)
        print("All tests completed!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the API is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")


