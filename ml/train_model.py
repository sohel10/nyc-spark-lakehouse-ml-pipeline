import pandas as pd
from sqlalchemy import create_engine
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib

print("Loading data from PostgreSQL...")

engine = create_engine("postgresql://postgres:postgres@localhost:5432/nyc_db")

# =========================
# LOAD DATA
# =========================
df = pd.read_sql("SELECT * FROM taxi_data", engine)

# Normalize column names
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

# Drop missing values
before_rows = len(df)
df = df.dropna(subset=["passenger_count", "trip_distance", "fare_amt", "month", "pickup_ts"])
after_rows = len(df)

print(f"Rows before dropna: {before_rows}")
print(f"Rows after dropna: {after_rows}")
print(f"Dropped rows: {before_rows - after_rows}")

# =========================
# FEATURE ENGINEERING 🔥
# =========================
df = df.copy()

# Convert types
df["pickup_ts"] = pd.to_datetime(df["pickup_ts"], errors="coerce")

# Extract time features
df["hour"] = df["pickup_ts"].dt.hour
df["day_of_week"] = df["pickup_ts"].dt.dayofweek

# Convert categorical
df["month"] = df["month"].astype("category")
df["hour"] = df["hour"].astype("category")
df["day_of_week"] = df["day_of_week"].astype("category")

# One-hot encoding
df = pd.get_dummies(df, columns=["month", "hour", "day_of_week"], drop_first=True)

# =========================
# FEATURES / TARGET
# =========================
feature_cols = (
    [col for col in df.columns if col.startswith("month_")] +
    [col for col in df.columns if col.startswith("hour_")] +
    [col for col in df.columns if col.startswith("day_of_week_")] +
    ["passenger_count", "trip_distance"]
)

X = df[feature_cols]
y = df["fare_amt"]

print("Features used:", feature_cols)

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
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

print("Training model...")
model.fit(X_train, y_train)

# =========================
# EVALUATION 🔥
# =========================
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"✅ RMSE: {rmse:.2f}")

# =========================
# FEATURE IMPORTANCE 🔥
# =========================
importances = model.feature_importances_

importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": importances
}).sort_values(by="importance", ascending=False)

print("\n🔥 Feature Importance:")
print(importance_df.to_string(index=False))

print("\n🔥 Feature Importance:")
print(importance_df.to_string(index=False))

# =========================
# VISUALIZE FEATURE IMPORTANCE 🔥
# =========================
import matplotlib.pyplot as plt
import os

output_dir = "docs/figures"
os.makedirs(output_dir, exist_ok=True)

# -------------------------
# Separate feature groups
# -------------------------
hour_imp = importance_df[importance_df["feature"].str.startswith("hour_")].copy()
dow_imp = importance_df[importance_df["feature"].str.startswith("day_of_week_")].copy()
month_imp = importance_df[importance_df["feature"].str.startswith("month_")].copy()

# -------------------------
# Extract numeric values
# -------------------------
hour_imp["hour"] = hour_imp["feature"].str.replace("hour_", "").astype(int)
dow_imp["dow"] = dow_imp["feature"].str.replace("day_of_week_", "").astype(int)
month_imp["month"] = month_imp["feature"].str.replace("month_", "").astype(int)

# -------------------------
# Label mapping
# -------------------------
dow_map = {
    0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu",
    4: "Fri", 5: "Sat", 6: "Sun"
}

month_map = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

hour_imp["label"] = hour_imp["hour"].astype(str) + ":00"
dow_imp["label"] = dow_imp["dow"].map(dow_map)
month_imp["label"] = month_imp["month"].map(month_map)

# -------------------------
# Plot: Hour importance
# -------------------------
hour_imp = hour_imp.sort_values("hour")

plt.figure()
plt.bar(hour_imp["label"], hour_imp["importance"])
plt.title("Feature Importance by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Importance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/hour_importance.png")
plt.close()

# -------------------------
# Plot: Day of week
# -------------------------
dow_imp = dow_imp.sort_values("dow")

plt.figure()
plt.bar(dow_imp["label"], dow_imp["importance"])
plt.title("Feature Importance by Day of Week")
plt.xlabel("Day")
plt.ylabel("Importance")
plt.tight_layout()
plt.savefig(f"{output_dir}/dow_importance.png")
plt.close()

# -------------------------
# Plot: Month
# -------------------------
month_imp = month_imp.sort_values("month")

plt.figure()
plt.bar(month_imp["label"], month_imp["importance"])
plt.title("Feature Importance by Month")
plt.xlabel("Month")
plt.ylabel("Importance")
plt.tight_layout()
plt.savefig(f"{output_dir}/month_importance.png")
plt.close()

print("✅ Feature importance plots saved!")

# =========================
# SAVE MODEL
# =========================
# =========================
# SAVE MODEL + FEATURES 🔥
# =========================
model_path = "/home/sohel/nyc-spark-pipeline/ml/model.pkl"
features_path = "/home/sohel/nyc-spark-pipeline/ml/features.pkl"

# Save model
joblib.dump(model, model_path)

# Save feature columns
joblib.dump(feature_cols, features_path)

print(f"✅ Model saved at {model_path}")
print(f"✅ Features saved at {features_path}")