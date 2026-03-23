from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import time
from pathlib import Path
from sqlalchemy import create_engine
from datetime import datetime

# =========================
# App
# =========================
# =========================
# Database
# =========================
DB_URL = "postgresql://postgres:1234@localhost:5432/nyc_taxi"
engine = create_engine(DB_URL)

app = FastAPI(
    title="NYC Taxi Fare Prediction API",
    version="1.0.0"
)

app.state.build_id = str(int(time.time()))

# Optional UI (keep for future)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# =========================
# Config
# =========================
MODEL_PATH = Path("/home/sohel/nyc-spark-pipeline/ml/model.pkl")

# =========================
# Request Schema
# =========================
class TaxiInput(BaseModel):
    passenger_count: int
    trip_distance: float

# =========================
# Globals
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
# API Endpoints
# =========================

@app.get("/health")
def health():
    return {"status": "healthy"}

# =========================
# Prediction API
# =========================
@app.post("/predict")
def predict(data: TaxiInput):
    
    input_df = pd.DataFrame([{
        "passenger_count": data.passenger_count,
        "trip_distance": data.trip_distance
    }])

    prediction = model.predict(input_df)[0]
    result = float(prediction)

    # ✅ Save to PostgreSQL
    save_df = pd.DataFrame([{
        "passenger_count": data.passenger_count,
        "trip_distance": data.trip_distance,
        "predicted_fare": result,
        "created_at": datetime.now()
    }])

    save_df.to_sql("taxi_prediction_logs", engine, if_exists="append", index=False)

    return {"predicted_fare": result}
# =========================
# UI (optional)
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
@app.get("/history")
def get_history():
    df = pd.read_sql(
        "SELECT * FROM taxi_prediction_logs ORDER BY created_at DESC LIMIT 10",
        engine
    )

    # ✅ Convert to ISO format (JS friendly)
    df["created_at"] = df["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df.to_dict(orient="records")