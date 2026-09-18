from pydantic import BaseModel, Field
from typing import Annotated, Dict

class PredictionDetail(BaseModel):
    predicted_category: Annotated[
        str,
        Field(..., description="Predicted insurance premium category", examples=["Medium"])
    ]
    confidence: Annotated[
        float,
        Field(..., description="Confidence score of the prediction", examples=[0.45])
    ]
    class_probabilities: Annotated[
        Dict[str, float],
        Field(
            ...,
            description="Probabilities for each prediction category",
            examples=[{"High": 0.36, "Low": 0.19, "Medium": 0.45}]
        )
    ]

class PredictionResponse(BaseModel):
    predicted_category: Annotated[
        str,
        Field(..., description="Predicted insurance premium category", examples=["Medium"])
    ]
    confidence: Annotated[
        float,
        Field(..., description="Confidence score of the prediction", examples=[0.45])
    ]
    class_probabilities: Annotated[
        Dict[str, float],
        Field(
            ...,
            description="Probabilities for each prediction category",
            examples=[{"High": 0.36, "Low": 0.19, "Medium": 0.45}]
        )
    ]
    response: Annotated[
        PredictionDetail,
        Field(..., description="Nested prediction details object")
    ]