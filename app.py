from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle
import pandas as pd

from schema.user_input import UserInput

""" import ML model """

MODEL_VERSION = "1.0.0"

with open('model/model.pkl','rb') as f:
    model = pickle.load(f)





app = FastAPI()

#human readable
@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API is running. Use /docs to test endpoints."}

#machine readable
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_version": MODEL_VERSION ,
        "model_loaded" :  model is not None
    }

@app.post("/predict")
def predict_premium(data: UserInput):
    # Normalize typo if present
    occupation = "business_owner" if data.occupation == "bussiness_owner" else data.occupation

    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': occupation
    }])
    
    prediction = str(model.predict(input_df)[0])
    probs = model.predict_proba(input_df)[0]
    classes = model.classes_
    class_probabilities = {str(c): round(float(p), 4) for c, p in zip(classes, probs)}
    confidence = round(float(max(probs)), 4)

    response_data = {
        "predicted_category": prediction,
        "confidence": confidence,
        "class_probabilities": class_probabilities
    }

    return JSONResponse(status_code=200, content={
        "predicted_category": prediction,
        "confidence": confidence,
        "class_probabilities": class_probabilities,
        "response": response_data
    })
