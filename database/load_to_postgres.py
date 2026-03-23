import pandas as pd
import glob
from sqlalchemy import create_engine

files = glob.glob("/home/sohel/nyc-spark-pipeline/outputs/sample_csv/*.csv")

df = pd.concat([pd.read_csv(f) for f in files])

engine = create_engine("postgresql://postgres:1234@localhost:5432/nyc_taxi")

df.to_sql("taxi_data", engine, if_exists="replace", index=False)

print("Loaded to Postgres")