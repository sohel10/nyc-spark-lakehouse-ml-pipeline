import pandas as pd
from sqlalchemy import create_engine
from xgboost import XGBRegressor
import joblib

print("Loading data from PostgreSQL...")

engine = create_engine("postgresql://postgres:1234@localhost:5432/nyc_taxi")

df = pd.read_sql("SELECT * FROM taxi_data", engine)

# 🔥 FIX: normalize column names
df.columns = df.columns.str.lower()

print("Columns:", df.columns)

# Features
# Correct features
X = df[[
    "passenger_count",
    "trip_distance"
]]

# Target
y = df["fare_amt"]

print("Training model...")

model = XGBRegressor(n_estimators=50, max_depth=3)
model.fit(X, y)

# Save model
joblib.dump(model, "/home/sohel/nyc-spark-pipeline/ml/model.pkl")

print("Model saved!")