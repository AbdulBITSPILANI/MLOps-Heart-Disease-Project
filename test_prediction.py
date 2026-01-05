"""
Simple script to test API predictions with custom input
"""

import requests
import json

# API URL
API_URL = "http://localhost:8000/predict"

# Sample input data - MODIFY THESE VALUES TO TEST DIFFERENT PATIENTS
input_data = {
    "age": 63,          # Age in years
    "sex": 1,           # 0=female, 1=male
    "cp": 3,            # Chest pain type (0-3)
    "trestbps": 145,    # Resting blood pressure (mm Hg)
    "chol": 233,        # Serum cholesterol (mg/dl)
    "fbs": 1,           # Fasting blood sugar > 120 mg/dl (0 or 1)
    "restecg": 0,       # Resting ECG results (0-2)
    "thalach": 150,     # Maximum heart rate achieved
    "exang": 0,         # Exercise induced angina (0 or 1)
    "oldpeak": 2.3,     # ST depression induced by exercise
    "slope": 0,         # Slope of peak exercise ST segment (0-2)
    "ca": 0,            # Number of major vessels (0-3)
    "thal": 1           # Thalassemia (0-3)
}

def make_prediction(data):
    """Make a prediction request to the API"""
    try:
        print("Sending prediction request...")
        print(f"Input data: {json.dumps(data, indent=2)}")
        print("\n" + "="*50)
        
        response = requests.post(API_URL, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction Successful!")
            print("="*50)
            print(f"Prediction: {'Heart Disease Present' if result['prediction'] == 1 else 'No Heart Disease'}")
            print(f"Probability: {result['probability']:.4f} ({result['probability']*100:.2f}%)")
            print(f"Confidence: {result['confidence']}")
            print("="*50)
            return result
        else:
            print(f"❌ Error: Status Code {response.status_code}")
            print(response.text)
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API.")
        print("Make sure the API is running: python src/api/main.py")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Heart Disease Prediction API - Test Script")
    print("="*50 + "\n")
    
    # Make prediction with default data
    result = make_prediction(input_data)
    
    # Example: Test with different patient data
    print("\n" + "="*50)
    print("Example: Testing with different patient data")
    print("="*50 + "\n")
    
    different_patient = {
        "age": 45,
        "sex": 0,
        "cp": 1,
        "trestbps": 130,
        "chol": 200,
        "fbs": 0,
        "restecg": 1,
        "thalach": 160,
        "exang": 0,
        "oldpeak": 1.0,
        "slope": 1,
        "ca": 0,
        "thal": 2
    }
    
    make_prediction(different_patient)

