# 🏦 Insurance Premium Predictor Service

An end-to-end Machine Learning API built with **FastAPI**, **Pydantic**, **Pandas**, and **Scikit-Learn**, designed to serve insurance premium predictions in real-time. This project follows production MLOps practices, progressing from local API development to containerization with Docker and cloud deployment on AWS.

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
- [ ] **Phase 2: Dockerization & Container Management (Upcoming)**
  - Create production-ready `Dockerfile` and `.dockerignore`.
  - Package dependencies, ML model artifact, and application environment into an isolated container.
  - Local container testing and port binding.
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
- **Containerization:** Docker *(Phase 2)*
- **Cloud Infrastructure:** AWS *(Phase 3)*

---

## 🚀 Getting Started Locally

### 1. Prerequisites
- Python 3.10+
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
