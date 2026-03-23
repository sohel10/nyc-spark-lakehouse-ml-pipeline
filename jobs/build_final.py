from pyspark.sql import SparkSession
from pyspark.sql.functions import month, col

def main():

    spark = SparkSession.builder \
    .appName("NYC Taxi Pipeline") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
    .getOrCreate()

    print("Reading data...")

    df = spark.read.parquet("/home/sohel/nyc-spark-pipeline/data_clean/2009.parquet")

    # ✅ VERY SMALL DATA (CRITICAL)
    df = df.limit(20000)
    df.coalesce(1).write.csv("outputs/sample_csv", header=True)
    df = df.withColumn("month", month(col("Trip_Pickup_DateTime")))

    print("Row count:", df.count())

    # ✅ NO Pandas, NO heavy write
    df.write.mode("overwrite").csv(
        "/home/sohel/nyc-spark-pipeline/outputs/sample_csv",
        header=True
    )

    print("Saved small CSV safely")

    spark.stop()

if __name__ == "__main__":
    main()