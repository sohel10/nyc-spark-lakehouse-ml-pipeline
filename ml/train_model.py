import pandas as pd
from sqlalchemy import create_engine
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib

print("Loading data from PostgreSQL...")

engine = create_engine("postgresql://postgres:postgres@localhost:5432/nyc_db")

df = pd.read_sql("SELECT * FROM taxi_data", engine)

df.columns = df.columns.str.lower()

print("Original rows:", len(df))

# =========================
# DATA CLEANING
# =========================
df = df[
    (df["passenger_count"] > 0) &
    (df["passenger_count"] <= 6) &
    (df["trip_distance"] > 0) &
    (df["trip_distance"] < 100) &
    (df["fare_amt"] > 0) &
    (df["fare_amt"] < 500)
]

print("Cleaned rows:", len(df))

# =========================
# FEATURES / TARGET
# =========================
X = df[["passenger_count", "trip_distance"]]
y = df["fare_amt"]

# =========================
# TRAIN / TEST SPLIT 🔥
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train size:", len(X_train))
print("Test size:", len(X_test))

# =========================
# MODEL
# =========================
model = XGBRegressor(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)

print("Training model...")
model.fit(X_train, y_train)

# =========================
# EVALUATION 🔥 (IMPORTANT)
# =========================
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"✅ RMSE: {rmse:.2f}")

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "/home/sohel/nyc-spark-pipeline/ml/model.pkl")

print("✅ Model saved!")