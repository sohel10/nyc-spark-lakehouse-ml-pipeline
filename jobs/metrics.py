from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("NYC_Metrics") \
        .getOrCreate()

    # Read processed analytical layer
    df = spark.read.parquet("data_clean/2009.parquet")

    total_rows = df.count()
    print("Total rows:", total_rows)

    print("\nRows per year:")
    df.groupBy("year").count().orderBy("year").show()

    print("\nNumber of Spark partitions:", df.rdd.getNumPartitions())

    spark.stop()

if __name__ == "__main__":
    main()