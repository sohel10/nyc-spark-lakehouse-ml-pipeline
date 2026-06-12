import os
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(title="Fare Analysis Dashboard")

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "ml"
TEMPLATES_DIR = BASE_DIR / "templates"

os.makedirs(BASE_DIR / "static", exist_ok=True)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

print("Loading models...")
model_2009 = joblib.load(MODELS_DIR / "model_2009.pkl")
model_2025 = joblib.load(MODELS_DIR / "model_2025.pkl")
print("✅ Models loaded")

FEATURES = ['passenger_count', 'trip_distance', 'distance_sq', 'hour', 'day_of_week', 'month']

class PredictionInput(BaseModel):
    passenger_count: int
    trip_distance: float
    hour: int
    day_of_week: int
    month: int

class PredictionResponse(BaseModel):
    fare: float

class ComparisonResponse(BaseModel):
    fare_2009: float
    fare_2025: float
    increase_percent: float

@app.get("/", response_class=FileResponse)
async def home():
    return FileResponse(TEMPLATES_DIR / "index.html", media_type="text/html")

@app.get("/2009", response_class=FileResponse)
async def page_2009():
    return FileResponse(TEMPLATES_DIR / "2009.html", media_type="text/html")

@app.get("/2025", response_class=FileResponse)
async def page_2025():
    return FileResponse(TEMPLATES_DIR / "2025.html", media_type="text/html")

@app.get("/comparison", response_class=FileResponse)
async def page_comparison():
    return FileResponse(TEMPLATES_DIR / "comparison.html", media_type="text/html")

@app.post("/api/predict/2009", response_model=PredictionResponse)
async def predict_2009(data: PredictionInput):
    try:
        input_df = pd.DataFrame([{
            'passenger_count': data.passenger_count,
            'trip_distance': data.trip_distance,
            'distance_sq': data.trip_distance ** 2,
            'hour': data.hour,
            'day_of_week': data.day_of_week,
            'month': data.month
        }])
        prediction = model_2009.predict(input_df[FEATURES])[0]
        return PredictionResponse(fare=float(max(0, prediction)))
    except Exception as e:
        return PredictionResponse(fare=0.0)

@app.post("/api/predict/2025", response_model=PredictionResponse)
async def predict_2025(data: PredictionInput):
    try:
        input_df = pd.DataFrame([{
            'passenger_count': data.passenger_count,
            'trip_distance': data.trip_distance,
            'distance_sq': data.trip_distance ** 2,
            'hour': data.hour,
            'day_of_week': data.day_of_week,
            'month': data.month
        }])
        prediction = model_2025.predict(input_df[FEATURES])[0]
        return PredictionResponse(fare=float(max(0, prediction)))
    except Exception as e:
        return PredictionResponse(fare=0.0)

@app.post("/api/compare", response_model=ComparisonResponse)
async def compare(data: PredictionInput):
    try:
        input_df = pd.DataFrame([{
            'passenger_count': data.passenger_count,
            'trip_distance': data.trip_distance,
            'distance_sq': data.trip_distance ** 2,
            'hour': data.hour,
            'day_of_week': data.day_of_week,
            'month': data.month
        }])
        fare_2009 = model_2009.predict(input_df[FEATURES])[0]
        fare_2025 = model_2025.predict(input_df[FEATURES])[0]
        if fare_2009 > 0:
            increase_percent = ((fare_2025 - fare_2009) / fare_2009) * 100
        else:
            increase_percent = 0
        return ComparisonResponse(
            fare_2009=float(max(0, fare_2009)),
            fare_2025=float(max(0, fare_2025)),
            increase_percent=float(increase_percent)
        )
    except Exception as e:
        return ComparisonResponse(fare_2009=0.0, fare_2025=0.0, increase_percent=0.0)

@app.get("/health")
async def health():
    return {"status": "✅ Running"}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("NYC TAXI FARE DASHBOARD")
    print("="*60)
    print("\n📊 VISIT:")
    print("  🏠 http://localhost:8000")
    print("  📈 http://localhost:8000/2009")
    print("  📊 http://localhost:8000/2025")
    print("  ⚖️  http://localhost:8000/comparison")
    print("\n👤 By: Sohel Ahmed")
    print("🔗 linkedin.com/in/sohelcu06")
    print("🐙 github.com/sohel10")
    print("📍 Michigan, USA")
    print("\n" + "="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
