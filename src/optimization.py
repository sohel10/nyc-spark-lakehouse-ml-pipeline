def write_partitioned(df):
    df.write \
      .mode("overwrite") \
      .partitionBy("year", "month") \
      .parquet("data_processed/")