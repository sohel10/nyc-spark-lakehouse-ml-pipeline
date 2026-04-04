from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator
import joblib
import pandas as pd
import time
from pathlib import Path
from sqlalchemy import create_engine
from datetime import datetime

# =========================
# Database
# =========================
DB_URL = "postgresql://postgres:postgres@localhost:5432/nyc_db"
engine = create_engine(DB_URL)

# =========================
# App
# =========================
app = FastAPI(
    title="NYC Taxi Fare Prediction API",
    version="1.0.0"
)

app.state.build_id = str(int(time.time()))

# Static + Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# =========================
# Model Path
# =========================
MODEL_PATH = Path("/home/sohel/nyc-spark-pipeline/ml/model.pkl")

# =========================
# Input Schema (WITH VALIDATION)
# =========================
class TaxiInput(BaseModel):
    passenger_count: int
    trip_distance: float

    @validator("passenger_count")
    def validate_passenger(cls, v):
        if v < 1 or v > 6:
            raise ValueError("Passenger count must be between 1 and 6")
        return v

    @validator("trip_distance")
    def validate_distance(cls, v):
        if v <= 0 or v > 100:
            raise ValueError("Trip distance must be between 0 and 100 miles")
        return v

# =========================
# Global Model
# =========================
model = None

# =========================
# Startup
# =========================
@app.on_event("startup")
def load_model():
    global model

    if not MODEL_PATH.exists():
        raise RuntimeError("❌ Model file not found")

    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")

# =========================
# Health Check
# =========================
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

# =========================
# Prediction Endpoint
# =========================
@app.post("/predict")
def predict(data: TaxiInput):
    try:
        # Prepare input
        input_df = pd.DataFrame([{
            "passenger_count": data.passenger_count,
            "trip_distance": data.trip_distance
        }])

        # Predict
        prediction = model.predict(input_df)[0]

        # Round + safety floor
        result = round(float(prediction), 2)
        result = max(result, 3.0)  # minimum fare

        # Save to DB
        save_df = pd.DataFrame([{
            "passenger_count": data.passenger_count,
            "trip_distance": data.trip_distance,
            "predicted_fare": result,
            "created_at": datetime.now()
        }])

        save_df.to_sql("taxi_prediction_logs", engine, if_exists="append", index=False)

        return {"predicted_fare": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# UI Home
# =========================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "build_id": app.state.build_id
        }
    )

# =========================
# History Endpoint
# =========================
@app.get("/history")
def get_history():
    df = pd.read_sql(
        "SELECT * FROM taxi_prediction_logs ORDER BY created_at DESC LIMIT 10",
        engine
    )

    df["created_at"] = df["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df.to_dict(orient="records")