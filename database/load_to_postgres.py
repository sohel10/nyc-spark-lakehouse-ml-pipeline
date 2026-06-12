import pandas as pd
from sqlalchemy import create_engine

# Read parquet
df = pd.read_parquet("data_single_10m/taxi_10m.parquet")

print("Loaded rows:", df.shape)

# Connect to PostgreSQL
engine = create_engine("postgresql://postgres:postgres@localhost:5432/nyc_db")

# Load with chunking (IMPORTANT)
df.to_sql(
    "taxi_data",
    engine,
    if_exists="replace",
    index=False,
    chunksize=100000
)

print("✅ Loaded to PostgreSQL")