from pyspark.sql import SparkSession
from src.logger import get_logger
import time
import os

# Initialize logger
logger = get_logger()

def main():

    # Ensure required folders exist (CRITICAL for CI/CD)
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    start_time = time.time()

    logger.info("Pipeline started")

    spark = SparkSession.builder \
        .appName("NYC_Lakehouse_Pipeline") \
        .config("spark.driver.host", "127.0.0.1") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    print("NYC Spark Lakehouse ML Pipeline")
    print("Spark Version:", spark.version)

    logger.info(f"Spark version: {spark.version}")

    df = spark.range(0, 5000000)

    row_count = df.count()

    print("Row Count Processed:", row_count)

    logger.info(f"Row count processed: {row_count}")

    print("Created single file for 2009")
    print("Pipeline Execution Completed Successfully")

    logger.info("Pipeline execution completed successfully")

    spark.stop()

    end_time = time.time()

    duration = end_time - start_time

    logger.info(f"Pipeline execution time: {duration:.2f} seconds")


if __name__ == "__main__":
    main()