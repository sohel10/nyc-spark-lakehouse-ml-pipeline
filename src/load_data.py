from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("NYC_Taxi_Partitioned") \
        .config("spark.driver.memory", "3g") \
        .config("spark.executor.memory", "3g") \
        .config("spark.sql.shuffle.partitions", "64") \
        .config("spark.default.parallelism", "64") \
        .config("spark.sql.files.maxPartitionBytes", "64MB") \
        .config("spark.sql.parquet.enableVectorizedReader", "false") \
        .getOrCreate()

    df = spark.read.parquet("data_raw/data/*/*.parquet")

    print("Total rows:", df.count())
    df.printSchema()

    spark.stop()

if __name__ == "__main__":
    main()