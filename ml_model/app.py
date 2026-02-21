# app.py

from fastapi import FastAPI
from pydantic import BaseModel
from model import train_model, predict

app = FastAPI()

class FeatureInput(BaseModel):
    features: list

@app.on_event("startup")
def startup_event():
    train_model()

@app.post("/predict")
def predict_anomaly(data: FeatureInput):
    prediction, score = predict(data.features)
    
    return {
        "anomaly": True if prediction == -1 else False,
        "score": float(score)
    }