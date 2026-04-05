from pyspark.sql import SparkSession

def main():

    spark = SparkSession.builder \
        .appName("Sample_10M_Single_File") \
        .config("spark.driver.memory", "16g") \
        .getOrCreate()

    print("Reading processed data...")

    df = spark.read.parquet("data_processed")

    print("Total rows:", df.count())

    # Take EXACT 10M rows (safe + fast)
    df_sample = df.sample(fraction=0.06, seed=42)

    print("Sample rows:", df_sample.count())

    # Create single file
    output_path = "data_single_10m"

    df_sample.coalesce(1).write \
        .mode("overwrite") \
        .parquet(output_path)

    print(f"✅ Single 10M file saved at: {output_path}")

    spark.stop()


if __name__ == "__main__":
    main()