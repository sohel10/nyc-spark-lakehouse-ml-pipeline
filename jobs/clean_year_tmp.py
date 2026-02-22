# jobs/clean_year_tmp.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from src.transformation import add_time_features
import glob
import os


def main():

    spark = SparkSession.builder \
        .appName("NYC_Taxi_Clean_TMP") \
        .master("local[*]") \
        .config("spark.sql.parquet.enableVectorizedReader", "false") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()

    base_path = "data_raw/data"
    years = ["2009"]  # change year here

    for year in years:

        print(f"\nProcessing year: {year}")

        year_folder = f"{base_path}/{year}"
        monthly_files = sorted(glob.glob(f"{year_folder}/*.parquet"))

        output_tmp_path = f"data_clean_tmp/{year}"

        for file in monthly_files:

            print(f"  Reading file: {os.path.basename(file)}")

            try:
                df = spark.read \
                    .option("mergeSchema", "false") \
                    .parquet(file)

                # Cast numeric columns safely
                numeric_columns = [
                    "Passenger_Count",
                    "Trip_Distance",
                    "Fare_Amt",
                    "Total_Amt",
                    "Rate_Code"
                ]

                for c in numeric_columns:
                    if c in df.columns:
                        df = df.withColumn(c, col(c).cast("double"))

                df = add_time_features(df)

                # small partitions → safe memory
                df = df.coalesce(4)

                df.write \
                    .mode("append") \
                    .option("compression", "snappy") \
                    .parquet(output_tmp_path)

            except Exception as e:
                print(f"❌ Failed file: {file}")
                print(e)
                continue

        print(f"✅ Finished temporary write for year {year}")

    spark.stop()


if __name__ == "__main__":
    main()