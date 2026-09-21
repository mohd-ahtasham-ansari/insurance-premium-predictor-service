# 🏦 Insurance Premium Predictor Service

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-mdahtasham112%2Finsurance--premium--api-blue?logo=docker&logoColor=white)](https://hub.docker.com/r/mdahtasham112/insurance-premium-api)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

An end-to-end Machine Learning API built with **FastAPI**, **Pydantic**, **Pandas**, and **Scikit-Learn**, designed to serve insurance premium predictions in real-time. This project follows production MLOps practices, progressing from local API development to containerization with Docker and cloud deployment on AWS.

🔗 **Docker Hub Image Repository:** [hub.docker.com/r/mdahtasham112/insurance-premium-api](https://hub.docker.com/r/mdahtasham112/insurance-premium-api)

---

## 📌 Project Overview

This service takes user demographic, lifestyle, and financial details, automatically engineers key health/risk features (such as **BMI**, **Lifestyle Risk**, **Age Group**, and **City Tier**), and passes them to a trained Scikit-learn model to predict the insurance premium category along with prediction confidence scores.

---

## 🎯 Project Roadmap & Status

- [x] **Phase 1: Local API Development & Feature Engineering (Completed)**
  - Built RESTful endpoints using **FastAPI**.
  - Strict payload validation and custom field normalization using **Pydantic**.
  - Dynamic feature engineering with `@computed_field` (BMI, Lifestyle Risk, Age Group, City Tier).
  - Model loading and inference with class confidence probabilities.
- [x] **Phase 2: Dockerization & Container Management (Completed & Verified ✅)**
  - Created production-ready `Dockerfile` and `.dockerignore`.
  - Packaged dependencies, ML model artifact, and application environment into an isolated container.
  - Successfully built, tagged, and published container image to [Docker Hub](https://hub.docker.com/r/mdahtasham112/insurance-premium-api).
  - **Pull & Run Verification:** Pulled image directly from Docker Hub, executed the container, and verified identical inference results with 100% parity against local development.
- [ ] **Phase 3: Cloud Deployment on AWS (Upcoming)**
  - Push Docker image to **AWS Elastic Container Registry (ECR)**.
  - Deploy application on **AWS App Runner** / **AWS ECS (Fargate)** or **EC2**.
  - Expose secure HTTPS endpoints for production consumption.
- [ ] **Phase 4: CI/CD & MLOps Automation (Upcoming)**
  - Set up **GitHub Actions** workflow for automated testing.
  - Auto-build and push Docker images to AWS on push to `main`.

---

## 🛠️ Architecture & Tech Stack

- **Framework:** FastAPI
- **Data Validation:** Pydantic (v2)
- **ML & Data Processing:** Scikit-Learn, Pandas, NumPy
- **Server:** Uvicorn
- **Containerization:** Docker (Published on Docker Hub)
- **Cloud Infrastructure:** AWS *(Phase 3)*

---

## 📁 Project Structure

```text
insurance-premium-prediction-API/
├── app.py                  # FastAPI application routes (/health, /predict)
├── Dockerfile              # Docker container definition
├── .dockerignore           # Excluded files from Docker build context
├── config/
│   └── city_tier.py        # City tier classification data
├── model/
│   ├── model.pkl           # Trained Scikit-Learn model artifact
│   └── predict.py          # Model loading & predict_output inference function
├── schema/
│   ├── prediction_response.py # Response validation schema
│   └── user_input.py       # Pydantic schema & computed fields (BMI, risk, etc.)
├── requirements.txt        # Dependency specification file
└── README.md               # Project documentation
```

---

## 🐳 Quickstart with Docker (Recommended)

You can run the service directly without setting up Python or installing local dependencies by using the pre-built Docker image from Docker Hub.

### 1. Pull the Docker Image
```bash
docker pull mdahtasham112/insurance-premium-api
```

### 2. Run the Container
```bash
docker run -d -p 8000:8000 --name insurance-api mdahtasham112/insurance-premium-api
```

### 3. Test & Verify the Running Container
```bash
# Health check test
curl http://localhost:8000/health

# Prediction endpoint test
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "weight": 70.0,
    "height": 1.75,
    "income_lpa": 12.5,
    "smoker": false,
    "city": "Mumbai",
    "occupation": "private_job"
  }'
```

Interactive Swagger UI is also accessible at: [http://localhost:8000/docs](http://localhost:8000/docs)

### (Optional) Build Locally from Source
```bash
docker build -t mdahtasham112/insurance-premium-api .
docker run -d -p 8000:8000 --name insurance-api mdahtasham112/insurance-premium-api
```

---

## 🚀 Getting Started Locally (Without Docker)

### 1. Prerequisites
- Python 3.12+
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/mohd-ahtasham-ansari/insurance-premium-predictor-service.git
cd insurance-premium-predictor-service
```

### 3. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the API Server
```bash
uvicorn app:app --reload
```
The server will start at `http://127.0.0.1:8000`.

---

## 📡 API Endpoints & Usage

### 1. Root Endpoint
- **URL:** `GET /`
- **Description:** Basic greeting and welcome message.

### 2. Health Check Endpoint
- **URL:** `GET /health`
- **Description:** Machine-readable health check endpoint.
- **Sample Response:**
```json
{
  "status": "ok",
  "model_version": "1.0.0",
  "model_loaded": true
}
```

### 3. Prediction Endpoint
- **URL:** `POST /predict`
- **Interactive Documentation:** Available at `http://127.0.0.1:8000/docs` (Swagger UI).
- **Sample Request Payload:**
```json
{
  "age": 30,
  "weight": 70.0,
  "height": 1.75,
  "income_lpa": 12.5,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

- **Sample Response:**
```json
{
  "predicted_category": "Medium",
  "confidence": 0.8542,
  "class_probabilities": {
    "Low": 0.1023,
    "Medium": 0.8542,
    "High": 0.0435
  },
  "response": {
    "predicted_category": "Medium",
    "confidence": 0.8542,
    "class_probabilities": {
      "Low": 0.1023,
      "Medium": 0.8542,
      "High": 0.0435
    }
  }
}
```

---

## 🧪 Computed Features & Engineering Rules

The API automatically computes derived features before passing input to the machine learning model:
- **BMI:** Computed dynamically from height and weight ($\text{BMI} = \frac{\text{weight}}{\text{height}^2}$).
- **Lifestyle Risk:** Assessed into `low`, `medium`, or `high` based on smoking status and BMI threshold.
- **Age Group:** Categorized into `young` (<25), `adult` (<45), `middle_aged` (<60), or `senior` ($\ge$60).
- **City Tier:** Classified into Tier 1, Tier 2, or Tier 3 depending on standard Indian city classification.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
