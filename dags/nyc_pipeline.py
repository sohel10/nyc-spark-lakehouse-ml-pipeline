from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import subprocess
import os
import pandas as pd
from sqlalchemy import create_engine

# =========================
# Database Connection
# =========================
engine = create_engine("postgresql://postgres:postgres@localhost:5432/nyc_db")

# =========================
# Default Args (Production)
# =========================
default_args = {
    "owner": "sohel",
    "start_date": datetime(2024, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
}

# =========================
# Task 0 — Create Tables
# =========================
def create_tables():
    env = os.environ.copy()
    env["PGPASSWORD"] = "1234"

    subprocess.run([
        "psql",
        "-U", "postgres",
        "-d", "nyc_taxi",
        "-f", "/home/sohel/nyc-spark-pipeline/sql/new_tables.sql"
    ], check=True, env=env)

# =========================
# Task 1 — Build Spark Data (BashOperator)
# =========================
# (Already handled in DAG)

# =========================
# Task 2 — Load Data to Postgres
# =========================
def run_load():
    subprocess.run([
        "/home/sohel/miniconda3/envs/mimic-spark/bin/python",
        "/home/sohel/nyc-spark-pipeline/database/load_to_postgres.py"
    ], check=True)

# =========================
# Task 3 — Data Validation (NEW 🔥)
# =========================
def validate_data():
    df = pd.read_sql("SELECT * FROM taxi_data LIMIT 1000", engine)

    if df.empty:
        raise ValueError("❌ Data validation failed: table is empty")

    # Missing values
    if df["trip_distance"].isnull().sum() > 0:
        raise ValueError("❌ Missing values in trip_distance")

    if df["passenger_count"].isnull().sum() > 0:
        raise ValueError("❌ Missing values in passenger_count")

    # Invalid values
    if (df["trip_distance"] <= 0).any():
        raise ValueError("❌ Invalid trip_distance (<=0)")

    if (df["passenger_count"] <= 0).any():
        raise ValueError("❌ Invalid passenger_count (<=0)")

    print("✅ Data validation passed")

# =========================
# Task 4 — Run SQL Analysis
# =========================
def run_sql():
    env = os.environ.copy()
    env["PGPASSWORD"] = "1234"

    subprocess.run([
        "psql",
        "-U", "postgres",
        "-d", "nyc_taxi",
        "-f", "/home/sohel/nyc-spark-pipeline/sql/analysis.sql"
    ], check=True, env=env)

# =========================
# Task 5 — Train Model
# =========================
def run_ml():
    subprocess.run([
        "/home/sohel/miniconda3/envs/mimic-spark/bin/python",
        "/home/sohel/nyc-spark-pipeline/ml/train_model.py"
    ], check=True)

# =========================
# DAG Definition
# =========================
with DAG(
    dag_id="nyc_taxi_pipeline",
    default_args=default_args,
    schedule=None,   # manual or weekly
    catchup=False,
    description="NYC Taxi End-to-End Training Pipeline with Validation"
) as dag:

    # Task 0: Create tables
    create_table_task = PythonOperator(
        task_id="create_tables",
        python_callable=create_tables
    )

    # Task 1: Build Spark Data
    build_task = BashOperator(
        task_id="build_spark_data",
        bash_command="""
        spark-submit \
        --master local[*] \
        --driver-memory 24g \
        --executor-memory 16g \
        --conf spark.sql.shuffle.partitions=200 \
        /home/sohel/nyc-spark-pipeline/jobs/build_final.py
        """
    )

    # Task 2: Load into PostgreSQL
    load_task = PythonOperator(
        task_id="load_postgres",
        python_callable=run_load
    )

    # Task 3: Validate Data
    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data
    )

    # Task 4: SQL Analysis
    sql_task = PythonOperator(
        task_id="run_sql_analysis",
        python_callable=run_sql
    )

    # Task 5: Train Model
    ml_task = BashOperator(
        task_id="train_xgboost_model",
        bash_command="""
        /home/sohel/miniconda3/envs/mimic-spark/bin/python \
        /home/sohel/nyc-spark-pipeline/ml/train_model.py
        """
    )

    # =========================
    # FINAL WORKFLOW
    # =========================
    create_table_task >> build_task >> load_task >> validate_task >> sql_task >> ml_task