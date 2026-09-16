from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field , field_validator
from typing import Annotated ,Literal
import pickle
import pandas as pd

""" import ML model """

MODEL_VERSION = "1.0.0"

with open('model/model.pkl','rb') as f:
    model = pickle.load(f)





app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

""" Pydantic model for data validation """
class UserInput(BaseModel):

    age: Annotated[int, Field(..., ge=0, lt=120, description="Age of the user")]
    weight: Annotated[float, Field(..., ge=0, lt=1000, description="Weight of the user in kg")]
    height: Annotated[float, Field(..., ge=0, lt=2.5, description="Height of the user in meter")]
    income_lpa: Annotated[float, Field(..., ge=0, lt=500, description="Income of the user in LPA")]
    smoker: Annotated[bool, Field(..., description="is user a smoker true or false")]
    city: Annotated[str, Field(..., description="city of the user ")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'bussiness_owner', 'unemployed', 'private_job'], Field(..., description="occupation of the user")]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

    @field_validator("city")
    @classmethod
    def normalize_city(cls , v:str)-> str:
        v=v.strip().title()
        return v

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
