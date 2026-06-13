import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Modeli yükleyelim
pipeline = joblib.load("saved_models/churn_pipeline.pkl")

app = FastAPI(title = "Churn Prediction API ")

#Kullanıcıdan gelecek istek şablonunu oluşturalım 

class CustomerInput(BaseModel):
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float

    class Config:
        json_schema_extra = {
            "example": {
                "CreditScore": 619,
                "Geography": "France",
                "Gender": "Female",
                "Age": 42,
                "Tenure": 2,
                "Balance": 0.0,
                "NumOfProducts": 1,
                "HasCrCard": 1,
                "IsActiveMember": 1,
                "EstimatedSalary": 101348.88
            }
        }

@app.get("/")
def root():
    return {"message": "Churn Prediction API is running!"}

@app.post("/predict")
def predict(input: CustomerInput):
    df = pd.DataFrame([input.model_dump()])
    
    # Tahmin yaptırmak
    prediction = pipeline.predict(df)[0]
    probability = pipeline.predict_proba(df)[0]
    
    return {
        "prediction": int(prediction),
        "result": "Customer will EXIT" if prediction == 1 else "Customer will STAY",
        "probability": {
            "stay": round(float(probability[0]), 4),
            "exit": round(float(probability[1]), 4)
        }
    }