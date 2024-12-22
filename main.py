from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import joblib

# Load the trained model
try:
    model = joblib.load("gaussian_nb_pipeline.pkl")
except FileNotFoundError:
    raise RuntimeError("Model file 'gaussian_nb_pipeline.pkl' not found. Ensure it is in the same directory as this script.")

# Initialize FastAPI app
app = FastAPI()

# Define input schema
class InputData(BaseModel):
    equipment_name: str  # Categorical feature
    location_name: str  # Categorical feature
    temperature: float  # Numerical feature
    pressure: float  # Numerical feature
    vibration: float  # Numerical feature
    humidity: float  # Numerical feature

# Define output schema
class PredictionResult(BaseModel):
    faulty: float  # 0 for No, 1 for Yes

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Fault Prediction API!"}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResult)
def predict(input_data: InputData):
    """
    Predict whether the equipment is faulty or not.
    """
    try:
        # Prepare input features in the correct order
        input_features = [[
            input_data.equipment_name,  # Categorical
            input_data.location_name,  # Categorical
            input_data.temperature,    # Numerical
            input_data.pressure,       # Numerical
            input_data.vibration,      # Numerical
            input_data.humidity        # Numerical
        ]]

        # Predict using the loaded model
        prediction = model.predict(input_features)

        # Return the result
        return {"faulty": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
