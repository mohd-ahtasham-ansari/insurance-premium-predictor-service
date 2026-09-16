from fastapi import FastAPI
from fastapi.responses import JSONResponse

from schema.user_input import UserInput
from model.predict import predict_output, MODEL_VERSION, model


app = FastAPI()

# human readable
@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API is running. Use /docs to test endpoints."}

# machine readable
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_version": MODEL_VERSION,
        "model_loaded": model is not None
    }

@app.post("/predict")
def predict_premium(data: UserInput):
    # Normalize typo if present
    occupation = "business_owner" if data.occupation == "bussiness_owner" else data.occupation

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': occupation
    }

    response_data = predict_output(user_input)

    return JSONResponse(status_code=200, content={
        "predicted_category": response_data["predicted_category"],
        "confidence": response_data["confidence"],
        "class_probabilities": response_data["class_probabilities"],
        "response": response_data
    })

