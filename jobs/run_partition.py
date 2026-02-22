from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from src.transformation import add_time_features
import os


def main():

    spark = SparkSession.builder \
        .appName("NYC_Taxi_Pipeline") \
        .master("local[*]") \
        .config("spark.driver.memory", "16g") \
        .config("spark.executor.memory", "16g") \
        .config("spark.sql.shuffle.partitions", "200") \
        .config("spark.default.parallelism", "200") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.files.maxPartitionBytes", "128MB") \
        .config("spark.sql.parquet.block.size", "134217728") \
        .config("spark.sql.parquet.enableVectorizedReader", "false") \
        .getOrCreate()

    base_path = "data_raw/data"
    years = sorted(os.listdir(base_path))

    for year in years:

        try:
            year_path = f"{base_path}/{year}/*.parquet"
            print(f"\nReading year: {year}")

            df_year = spark.read \
                .format("parquet") \
                .option("mergeSchema", "false") \
                .load(year_path)

            # Normalize numeric columns safely
            numeric_columns = [
                "Passenger_Count",
                "Trip_Distance",
                "Fare_Amt",
                "Total_Amt",
                "Rate_Code"
            ]

            for c in numeric_columns:
                if c in df_year.columns:
                    df_year = df_year.withColumn(c, col(c).cast("double"))

            # Add time features
            df_year = add_time_features(df_year)

            # Reduce partitions (safer for laptop)
            df_year = df_year.coalesce(8)

            # Write safely
            df_year.write \
                .mode("append") \
                .partitionBy("year", "month") \
                .parquet("data_processed")

            print(f"Finished year: {year}")

        except Exception as e:
            print(f"Error processing year {year}: {e}")
            break

    spark.stop()


if __name__ == "__main__":
    main()