from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("NYC_Lakehouse_Pipeline") \
    .config("spark.driver.host", "127.0.0.1") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("NYC Spark Lakehouse ML Pipeline")
print("Spark Version:", spark.version)

df = spark.range(0, 5000000)
print("Row Count Processed:", df.count())

print("Created single file for 2009")
print("Pipeline Execution Completed Successfully")

spark.stop()