from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import subprocess
import os
import pandas as pd
from sqlalchemy import create_engine

# =========================
# CONFIG (SINGLE SOURCE OF TRUTH 🔥)
# =========================
DB_URL = "postgresql://postgres:postgres@localhost:5432/nyc_db"
engine = create_engine(DB_URL)

# =========================
# DEFAULT ARGS
# =========================
default_args = {
    "owner": "sohel",
    "start_date": datetime(2024, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
}

# =========================
# TASK 0 — CREATE TABLES
# =========================
def create_tables():
    env = os.environ.copy()
    env["PGPASSWORD"] = "postgres"

    subprocess.run([
        "psql",
        "-h", "localhost",   # ✅ ADD THIS LINE
        "-p", "5432",        # ✅ (optional but good)
        "-U", "postgres",
        "-d", "nyc_db",
        "-f", "/home/sohel/nyc-spark-pipeline/sql/new_tables.sql"
    ], check=True, env=env)

# =========================
# TASK 2 — LOAD DATA
# =========================
def run_load():
    subprocess.run([
        "/home/sohel/miniconda3/envs/mimic-spark/bin/python",
        "/home/sohel/nyc-spark-pipeline/database/load_to_postgres.py"
    ], check=True)

# =========================
# TASK 3 — VALIDATION
# =========================
def validate_data():
    df = pd.read_sql("SELECT * FROM taxi_data LIMIT 1000", engine)

    if df.empty:
        raise ValueError("❌ Data validation failed: table is empty")

    if df["trip_distance"].isnull().any():
        raise ValueError("❌ Missing trip_distance")

    if df["passenger_count"].isnull().any():
        raise ValueError("❌ Missing passenger_count")

    if (df["trip_distance"] <= 0).any():
        raise ValueError("❌ Invalid trip_distance")

    if (df["passenger_count"] <= 0).any():
        raise ValueError("❌ Invalid passenger_count")

    print("✅ Data validation passed")

# =========================
# TASK 4 — SQL ANALYSIS
# =========================
def run_sql():
    env = os.environ.copy()
    env["PGPASSWORD"] = "postgres"

    subprocess.run([
        "psql",
        "-U", "postgres",
        "-d", "nyc_db",
        "-f", "/home/sohel/nyc-spark-pipeline/sql/analysis.sql"
    ], check=True, env=env)

# =========================
# DAG
# =========================
with DAG(
    dag_id="nyc_taxi_pipeline",
    default_args=default_args,
    schedule=None,
    catchup=False,
    description="NYC Taxi End-to-End ML Pipeline"
) as dag:

    create_table_task = PythonOperator(
        task_id="create_tables",
        python_callable=create_tables
    )

    build_task = BashOperator(
    task_id="build_spark_data",
    bash_command="""
    spark-submit \
    --master local[*] \
    --driver-memory 4g \
    --executor-memory 2g \
    /home/sohel/nyc-spark-pipeline/jobs/build_final.py
    """
    )

    load_task = PythonOperator(
        task_id="load_postgres",
        python_callable=run_load
    )

    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data
    )

    sql_task = PythonOperator(
        task_id="run_sql_analysis",
        python_callable=run_sql
    )

    ml_task = BashOperator(
        task_id="train_model",
        bash_command="""
        /home/sohel/miniconda3/envs/mimic-spark/bin/python \
        /home/sohel/nyc-spark-pipeline/ml/train_model.py
        """
    )

    # FLOW
    create_table_task >> build_task >> load_task >> validate_task >> sql_task >> ml_task