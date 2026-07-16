# 002 - Building an ML API (FastAPI / Flask)

## Concept
Wrapping a trained model in a small web API turns it from a static file into something other applications (a website, a mobile app, another service) can call over HTTP to get predictions in real time.

## Why It Matters
This is the most common way ML models are actually consumed in production. Both FastAPI (modern, async, auto-generates docs) and Flask (simpler, very widely used) are standard choices — knowing both is useful.

## Hands-On

```python
# pip install fastapi uvicorn flask --break-system-packages

# ============================================
# 1. FastAPI version - save as fastapi_app.py
# ============================================
"""
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Breast Cancer Classifier API")
model = joblib.load("model.joblib")

class PredictionRequest(BaseModel):
    features: list[float]   # exactly n_features_in_ values, in the correct order

class PredictionResponse(BaseModel):
    prediction: int
    confidence: float

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    X = np.array(request.features).reshape(1, -1)
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0].max()
    return PredictionResponse(prediction=int(pred), confidence=float(proba))

# Run with: uvicorn fastapi_app:app --reload
# Auto docs available at: http://localhost:8000/docs
"""

# ============================================
# 2. Flask version - save as flask_app.py
# ============================================
"""
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("model.joblib")

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    X = np.array(data["features"]).reshape(1, -1)
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0].max()
    return jsonify({"prediction": int(pred), "confidence": float(proba)})

# Run with: python flask_app.py (add app.run(debug=True) at the bottom)
"""

# ============================================
# 3. Client code to call either API
# ============================================
import requests

def call_prediction_api(features, url="http://localhost:8000/predict"):
    response = requests.post(url, json={"features": features})
    response.raise_for_status()
    return response.json()

# Example (requires the server running):
# sample_features = [14.2, 20.1, 91.3, ...]  # 30 values for breast cancer dataset
# result = call_prediction_api(sample_features)
# print(result)

# ============================================
# 4. Basic input validation - a common real bug source
# ============================================
def validate_features(features, expected_len=30):
    if not isinstance(features, list):
        raise ValueError("features must be a list")
    if len(features) != expected_len:
        raise ValueError(f"Expected {expected_len} features, got {len(features)}")
    if any(not isinstance(f, (int, float)) for f in features):
        raise ValueError("All features must be numeric")
    return True
```

## Exercise
1. Run the FastAPI version locally and open `/docs` in a browser — try calling `/predict` directly from the auto-generated Swagger UI.
2. Add a `/predict_batch` endpoint that accepts a list of feature lists and returns predictions for all of them in one call.
3. Add basic error handling: return a 400 status code with a clear message if `validate_features` fails.

## Key Takeaways
- FastAPI's type hints (via Pydantic models) give you automatic request validation and interactive documentation for free — a big advantage over Flask for ML APIs.
- Always add a `/health` endpoint — load balancers and orchestration systems (like Kubernetes) use it to know if your service is alive.
- Load the model **once** at startup (module-level, not inside the request handler) — reloading it on every request is slow and wasteful.
