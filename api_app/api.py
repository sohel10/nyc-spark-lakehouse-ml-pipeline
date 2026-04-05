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

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# =========================
# Paths
# =========================
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR.parent / "ml" / "model.pkl"
FEATURES_PATH = BASE_DIR.parent / "ml" / "features.pkl"
# =========================
# Input Schema
# =========================
class TaxiInput(BaseModel):
    passenger_count: int
    trip_distance: float
    pickup_ts: str  # 🔥 NEW

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
# Globals
# =========================
model = None
feature_cols = None

# =========================
# Startup
# =========================
@app.on_event("startup")
def load_model():
    global model, feature_cols

    if not MODEL_PATH.exists():
        raise RuntimeError("❌ Model file not found")

    if not FEATURES_PATH.exists():
        raise RuntimeError("❌ Feature list not found")

    model = joblib.load(MODEL_PATH)
    feature_cols = joblib.load(FEATURES_PATH)

    print("✅ Model + features loaded")

# =========================
# Feature Engineering (IMPORTANT)
# =========================
def prepare_features(data: TaxiInput):
    df = pd.DataFrame([{
        "passenger_count": data.passenger_count,
        "trip_distance": data.trip_distance,
        "pickup_ts": data.pickup_ts
    }])

    # Convert time
    df["pickup_ts"] = pd.to_datetime(df["pickup_ts"], errors="coerce")

    df["month"] = df["pickup_ts"].dt.month
    df["hour"] = df["pickup_ts"].dt.hour
    df["day_of_week"] = df["pickup_ts"].dt.dayofweek

    # One-hot encode
    df = pd.get_dummies(df, columns=["month", "hour", "day_of_week"], drop_first=True)

    # Align with training features
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_cols]

    return df

# =========================
# Prediction Endpoint
# =========================
@app.post("/predict")
def predict(data: TaxiInput):
    try:
        input_df = prepare_features(data)

        prediction = model.predict(input_df)[0]

        result = round(float(prediction), 2)
        result = max(result, 3.0)

        # Save
        save_df = pd.DataFrame([{
            "passenger_count": data.passenger_count,
            "trip_distance": data.trip_distance,
            "pickup_ts": data.pickup_ts,
            "predicted_fare": result,
            "created_at": datetime.now()
        }])

        save_df.to_sql("taxi_prediction_logs", engine, if_exists="append", index=False)

        return {"predicted_fare": result}

    except Exception as e:
        print("❌ ERROR:", str(e))   # 👈 VERY IMPORTANT
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# Health
# =========================
@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

# =========================
# UI
# =========================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "build_id": app.state.build_id}
    )

# =========================
# History
# =========================
@app.get("/history")
def get_history():
    df = pd.read_sql(
        "SELECT * FROM taxi_prediction_logs ORDER BY created_at DESC LIMIT 10",
        engine
    )

    df["created_at"] = df["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df.to_dict(orient="records")