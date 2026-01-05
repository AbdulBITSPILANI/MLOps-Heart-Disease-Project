# How to Give Inputs to the API

There are several ways to send input data to the prediction API. Here are the easiest methods:

## Method 1: Interactive API Documentation (Easiest! 🎯)

1. Start the API:
   ```bash
   python src/api/main.py
   ```

2. Open your browser and go to:
   ```
   http://localhost:8000/docs
   ```

3. Find the `/predict` endpoint and click "Try it out"

4. Click on the request body area and you'll see a sample JSON. Edit it with your values:

   ```json
   {
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
   ```

5. Click "Execute" button

6. See the prediction result below!

## Method 2: Using the Test Script

The easiest command-line method:

```bash
python scripts/test_api.py
```

This automatically uses the sample input file and shows you the result.

## Method 3: Using curl (Command Line)

```bash
curl -X POST "http://localhost:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"age\":63,\"sex\":1,\"cp\":3,\"trestbps\":145,\"chol\":233,\"fbs\":1,\"restecg\":0,\"thalach\":150,\"exang\":0,\"oldpeak\":2.3,\"slope\":0,\"ca\":0,\"thal\":1}"
```

Or using the sample file:
```bash
curl -X POST "http://localhost:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d @data/sample_input.json
```

## Method 4: Using Python

Create a Python script:

```python
import requests
import json

# Input data
input_data = {
    "age": 63,
    "sex": 1,              # 0=female, 1=male
    "cp": 3,               # Chest pain type (0-3)
    "trestbps": 145,       # Resting blood pressure
    "chol": 233,           # Serum cholesterol
    "fbs": 1,              # Fasting blood sugar > 120 (0 or 1)
    "restecg": 0,          # Resting ECG results (0-2)
    "thalach": 150,        # Maximum heart rate achieved
    "exang": 0,            # Exercise induced angina (0 or 1)
    "oldpeak": 2.3,        # ST depression
    "slope": 0,            # Slope of peak exercise ST segment (0-2)
    "ca": 0,               # Number of major vessels (0-3)
    "thal": 1              # Thalassemia (0-3)
}

# Make prediction
response = requests.post(
    "http://localhost:8000/predict",
    json=input_data
)

# Print result
print("Status Code:", response.status_code)
print("Prediction Result:")
print(json.dumps(response.json(), indent=2))
```

## Method 5: Using the Sample Input File

Edit `data/sample_input.json` with your values, then:

```bash
# Using Python
python -c "import requests, json; data=json.load(open('data/sample_input.json')); print(json.dumps(requests.post('http://localhost:8000/predict', json=data).json(), indent=2))"
```

## Input Field Descriptions

| Field | Description | Valid Range |
|-------|-------------|-------------|
| `age` | Age in years | 0-120 |
| `sex` | Sex | 0 (female), 1 (male) |
| `cp` | Chest pain type | 0-3 |
| `trestbps` | Resting blood pressure (mm Hg) | 0+ |
| `chol` | Serum cholesterol (mg/dl) | 0+ |
| `fbs` | Fasting blood sugar > 120 mg/dl | 0 or 1 |
| `restecg` | Resting electrocardiographic results | 0-2 |
| `thalach` | Maximum heart rate achieved | 0+ |
| `exang` | Exercise induced angina | 0 or 1 |
| `oldpeak` | ST depression induced by exercise | 0+ |
| `slope` | Slope of peak exercise ST segment | 0-2 |
| `ca` | Number of major vessels colored by flourosopy | 0-3 |
| `thal` | Thalassemia | 0-3 |

## Example Response

When you send a request, you'll get a response like this:

```json
{
  "prediction": 0,
  "probability": 0.19,
  "confidence": "Low"
}
```

Where:
- **prediction**: `0` = No heart disease, `1` = Heart disease present
- **probability**: Probability of heart disease (0.0 to 1.0)
- **confidence**: "Low", "Medium", or "High" based on probability

## Quick Test Examples

### Example 1: Low risk patient
```json
{
  "age": 35,
  "sex": 0,
  "cp": 0,
  "trestbps": 120,
  "chol": 180,
  "fbs": 0,
  "restecg": 0,
  "thalach": 175,
  "exang": 0,
  "oldpeak": 0.0,
  "slope": 1,
  "ca": 0,
  "thal": 2
}
```

### Example 2: High risk patient
```json
{
  "age": 70,
  "sex": 1,
  "cp": 2,
  "trestbps": 180,
  "chol": 280,
  "fbs": 1,
  "restecg": 1,
  "thalach": 120,
  "exang": 1,
  "oldpeak": 3.5,
  "slope": 0,
  "ca": 2,
  "thal": 3
}
```

## Troubleshooting

### "422 Unprocessable Entity" Error
- Check that all 13 fields are provided
- Verify values are within valid ranges
- Ensure JSON format is correct

### "Connection Error"
- Make sure the API is running (`python src/api/main.py`)
- Use `http://localhost:8000` (not `0.0.0.0:8000`)

### "Model not available" Error
- Train the model first: `python src/models/train.py`
- Check that `models/production_model.pkl` exists

