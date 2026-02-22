# jobs/build_final.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def main():

    spark = SparkSession.builder \
        .appName("NYC_Taxi_Final_Build") \
        .master("local[*]") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.shuffle.partitions", "128") \
        .getOrCreate()

    print("Reading cleaned yearly data...")
    df = spark.read.parquet("data_clean")

    print("Repartitioning...")
    df = df.repartition(128, col("year"), col("month"))

    print("Writing final dataset...")
    df.write \
        .mode("overwrite") \
        .option("compression", "snappy") \
        .partitionBy("year", "month") \
        .parquet("data_processed")

    print("Final build complete.")

    spark.stop()


if __name__ == "__main__":
    main()