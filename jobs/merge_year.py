# jobs/merge_year.py

from pyspark.sql import SparkSession


def main():

    spark = SparkSession.builder \
        .appName("Merge_Year_To_Single_File") \
        .master("local[*]") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()

    years = ["2009"]  # change manually

    for year in years:

        print(f"\nMerging year: {year}")

        input_path = f"data_clean_tmp/{year}"
        output_path = f"data_clean/{year}.parquet"

        df = spark.read.parquet(input_path)

        # Force single file
        df.coalesce(1) \
          .write \
          .mode("overwrite") \
          .option("compression", "snappy") \
          .parquet(output_path)

        print(f"✅ Created single file for {year}")

    spark.stop()


if __name__ == "__main__":
    main()