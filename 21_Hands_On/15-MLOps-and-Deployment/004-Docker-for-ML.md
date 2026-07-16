# 004 - Docker for ML

## Concept
Docker packages your model, code, and all dependencies into a single portable "container image" that runs identically on any machine — your laptop, a teammate's laptop, or a cloud server — eliminating "it works on my machine" problems.

## Why It Matters
Production ML systems almost always run inside containers, because it makes deployment reproducible and lets orchestration tools (Kubernetes, ECS, etc.) manage scaling and restarts consistently.

## Hands-On

```dockerfile
# ============================================
# Dockerfile - save this exact content as "Dockerfile" (no extension)
# ============================================

# 1. Start from a lightweight official Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements file first (Docker layer caching optimization -
#    dependencies rarely change, so this avoids reinstalling them on every code change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application code and the trained model
COPY app.py .
COPY model.joblib .

# 5. Expose the port the API listens on
EXPOSE 8000

# 6. The command that runs when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```text
# requirements.txt
fastapi==0.110.0
uvicorn==0.27.0
scikit-learn==1.4.0
joblib==1.3.2
numpy==1.26.4
```

```python
# app.py - minimal FastAPI app referenced by the Dockerfile
from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()
model = joblib.load("model.joblib")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(features: list[float]):
    X = np.array(features).reshape(1, -1)
    pred = model.predict(X)[0]
    return {"prediction": int(pred)}
```

```bash
# ============================================
# Build and run commands (run these in your terminal, not Python)
# ============================================

# Build the image, tagging it "ml-api:v1"
docker build -t ml-api:v1 .

# Run the container, mapping container port 8000 to host port 8000
docker run -p 8000:8000 ml-api:v1

# Check it's running
curl http://localhost:8000/health

# List running containers
docker ps

# View logs from a running container
docker logs <container_id>

# Stop it
docker stop <container_id>
```

```dockerfile
# ============================================
# Multi-stage build - smaller final image, useful for heavier ML deps
# ============================================
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py model.joblib ./
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Exercise
1. Build and run the image locally (if Docker is available in your environment) and confirm `curl http://localhost:8000/health` returns `{"status": "ok"}`.
2. Add a `.dockerignore` file that excludes `__pycache__`, `.git`, and any local virtual environment folders from the build context.
3. Measure image size with `docker images` for the single-stage vs. multi-stage build — how much smaller is the multi-stage version?

## Key Takeaways
- Copying `requirements.txt` and installing dependencies *before* copying application code takes advantage of Docker's layer caching — rebuilds are much faster when only code (not dependencies) changes.
- `python:3.11-slim` is a good default base image — smaller than the full `python:3.11` image, without the bloat of building from scratch.
- The exact same Docker image that runs on your laptop is what gets pushed to a container registry and deployed to production — this is the core promise of containerization.
