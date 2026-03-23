import pandas as pd
from sqlalchemy import create_engine
import joblib

print("Loading model...")
model = joblib.load("/home/sohel/nyc-spark-pipeline/ml/model.pkl")

print("Loading data...")
engine = create_engine("postgresql://postgres:1234@localhost:5432/nyc_taxi")
df = pd.read_sql("SELECT * FROM taxi_data", engine)

# normalize columns
df.columns = df.columns.str.lower()

# features
X = df[[
    "passenger_count",
    "trip_distance"
]]
print("Generating predictions...")
df["predicted_fare"] = model.predict(X)

print("Saving predictions to PostgreSQL...")
df.to_sql("taxi_predictions", engine, if_exists="replace", index=False)

print("Predictions saved!")
