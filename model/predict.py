import pickle
import pandas as pd


""" import ML model """

MODEL_VERSION = "1.0.0"

with open('model/model.pkl','rb') as f:
    model = pickle.load(f)


def predict_output(user_input: dict) -> dict:
    """
    Given a user input dictionary of processed features, 
    returns predicted category, confidence score, and class probabilities.
    """
    input_df = pd.DataFrame([user_input])

    prediction = str(model.predict(input_df)[0])
    probs = model.predict_proba(input_df)[0]
    classes = model.classes_
    class_probabilities = {str(c): round(float(p), 4) for c, p in zip(classes, probs)}
    confidence = round(float(max(probs)), 4)

    return {
        "predicted_category": prediction,
        "confidence": confidence,
        "class_probabilities": class_probabilities
    }