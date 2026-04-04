import pandas as pd
from sqlalchemy import create_engine
import numpy as np

engine = create_engine("postgresql://postgres:postgres@localhost:5432/nyc_db")

df = pd.DataFrame({
    "passenger_count": np.random.randint(1, 6, 1000),
    "trip_distance": np.random.uniform(1, 20, 1000),
})

df["fare_amt"] = 3 + df["trip_distance"] * 2.5 + np.random.normal(0, 2, 1000)

df.to_sql("taxi_data", engine, if_exists="replace", index=False)

print("✅ taxi_data table created")
