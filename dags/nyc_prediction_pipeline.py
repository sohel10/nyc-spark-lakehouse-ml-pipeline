from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import joblib
from sqlalchemy import create_engine

# =========================
# Config
# =========================
MODEL_PATH = "/home/sohel/nyc-spark-pipeline/ml/model.pkl"
DB_URL = "postgresql://postgres:1234@localhost:5432/nyc_taxi"

engine = create_engine(DB_URL)

# =========================
# Task 1 — Load new data
# =========================
def load_data(**context):
    # Example: simulate new incoming data
    df = pd.DataFrame({
        "passenger_count": [1, 2, 3, 4],
        "trip_distance": [2.5, 5.0, 7.2, 10.1]
    })

    # Save to temp file (Airflow XCom alternative)
    df.to_csv("/tmp/new_data.csv", index=False)

# =========================
# Task 2 — Predict
# =========================
def run_prediction(**context):
    df = pd.read_csv("/tmp/new_data.csv")

    model = joblib.load(MODEL_PATH)

    df["predicted_fare"] = model.predict(df)

    df.to_csv("/tmp/predictions.csv", index=False)

# =========================
# Task 3 — Save to PostgreSQL
# =========================
def save_to_db(**context):
    df = pd.read_csv("/tmp/predictions.csv")

    df["created_at"] = datetime.now()

    df.to_sql(
        "taxi_prediction_logs",
        engine,
        if_exists="append",
        index=False
    )

# =========================
# DAG Definition
# =========================
default_args = {
    "owner": "sohel",
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}

dag = DAG(
    "nyc_taxi_prediction_pipeline",
    default_args=default_args,
    schedule_interval="@daily",   # run daily
    catchup=False
)

# =========================
# Tasks
# =========================
task_load = PythonOperator(
    task_id="load_data",
    python_callable=load_data,
    dag=dag
)

task_predict = PythonOperator(
    task_id="run_prediction",
    python_callable=run_prediction,
    dag=dag
)

task_save = PythonOperator(
    task_id="save_to_db",
    python_callable=save_to_db,
    dag=dag
)

# =========================
# Workflow
# =========================
task_load >> task_predict >> task_save