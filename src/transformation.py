from pyspark.sql.functions import year, month, to_timestamp


def add_time_features(df):

    if "pickup_datetime" in df.columns:
        pickup_col = "pickup_datetime"
    elif "Trip_Pickup_DateTime" in df.columns:
        pickup_col = "Trip_Pickup_DateTime"
    else:
        raise Exception("Pickup datetime column not found.")

    df = df.withColumn(
        "pickup_ts",
        to_timestamp(pickup_col)
    )

    df = df.withColumn("year", year("pickup_ts"))
    df = df.withColumn("month", month("pickup_ts"))

    return df