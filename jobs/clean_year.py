# jobs/clean_year.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from src.transformation import add_time_features
import os
import glob


def main():

    spark = SparkSession.builder \
        .appName("NYC_Taxi_Clean_Year") \
        .master("local[*]") \
        .config("spark.sql.parquet.enableVectorizedReader", "false") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()

    base_path = "data_raw/data"
    years = ["2009"]   # change manually

    for year in years:

        print(f"\nProcessing year: {year}")

        year_folder = f"{base_path}/{year}"
        monthly_files = sorted(glob.glob(f"{year_folder}/*.parquet"))

        output_path = f"data_clean/{year}"

        for file in monthly_files:

            print(f"  Reading file: {os.path.basename(file)}")

            try:
                df = spark.read \
                    .option("mergeSchema", "false") \
                    .parquet(file)

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

                df = df.coalesce()   # smaller write partitions

                df.write \
                    .mode("append") \
                    .option("compression", "snappy") \
                    .parquet(output_path)

            except Exception as e:
                print(f"  ❌ Failed file: {file}")
                print(e)
                continue

        print(f"✅ Finished year: {year}")

    spark.stop()


if __name__ == "__main__":
    main()