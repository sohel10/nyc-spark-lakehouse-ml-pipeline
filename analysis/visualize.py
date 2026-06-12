import os
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# Setup
# =========================
engine = create_engine("postgresql://postgres:postgres@localhost:5432/nyc_db")

output_dir = "docs/figures"
os.makedirs(output_dir, exist_ok=True)

# =========================
# 1. Fare vs Distance
# =========================
query1 = """
SELECT 
  FLOOR("Trip_Distance") AS distance_bin,
  AVG("Fare_Amt") AS avg_fare
FROM taxi_data
WHERE "Trip_Distance" < 20
GROUP BY distance_bin
ORDER BY distance_bin;
"""

df1 = pd.read_sql(query1, engine)

plt.figure()
plt.plot(df1["distance_bin"], df1["avg_fare"], marker='o')
plt.xlabel("Trip Distance (miles)")
plt.ylabel("Average Fare ($)")
plt.title("Fare vs Distance")
plt.grid()
plt.savefig(f"{output_dir}/fare_vs_distance.png")
plt.close()

# =========================
# 2. Fare Distribution
# =========================
query2 = 'SELECT "Fare_Amt" FROM taxi_data WHERE "Fare_Amt" < 100;'
df2 = pd.read_sql(query2, engine)

plt.figure()
plt.hist(df2["Fare_Amt"], bins=50)
plt.title("Fare Distribution")
plt.xlabel("Fare ($)")
plt.ylabel("Frequency")
plt.savefig(f"{output_dir}/fare_distribution.png")
plt.close()

# =========================
# 3. Passenger Count
# =========================
query3 = """
SELECT "Passenger_Count", COUNT(*) as trips
FROM taxi_data
GROUP BY "Passenger_Count"
ORDER BY "Passenger_Count";
"""
df3 = pd.read_sql(query3, engine)

plt.figure()
plt.bar(df3["Passenger_Count"], df3["trips"])
plt.title("Passenger Count Distribution")
plt.xlabel("Passengers")
plt.ylabel("Trips")
plt.savefig(f"{output_dir}/passenger_distribution.png")
plt.close()

# =========================
# 4. Correlation Heatmap
# =========================
query4 = """
SELECT "Trip_Distance", "Fare_Amt", "Tip_Amt", "Total_Amt"
FROM taxi_data
LIMIT 100000;
"""
df4 = pd.read_sql(query4, engine)

corr = df4.corr()

plt.figure()
sns.heatmap(corr, annot=True)
plt.title("Correlation Matrix")
plt.savefig(f"{output_dir}/correlation_heatmap.png")
plt.close()

print("✅ All plots saved to docs/figures/")


# =========================
# 5. Monthly Revenue Trend
# =========================
query5 = """
SELECT 
  month,
  SUM("Total_Amt") AS revenue
FROM taxi_data
GROUP BY month
ORDER BY month;
"""

df5 = pd.read_sql(query5, engine)

plt.figure()
plt.plot(df5["month"], df5["revenue"], marker='o')
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue ($)")
plt.grid()
plt.savefig(f"{output_dir}/monthly_revenue.png")
plt.close()


# =========================
# 6. Monthly Average Fare
# =========================
query6 = """
SELECT 
  month,
  AVG("Fare_Amt") AS avg_fare
FROM taxi_data
GROUP BY month
ORDER BY month;
"""

df6 = pd.read_sql(query6, engine)

plt.figure()
plt.plot(df6["month"], df6["avg_fare"], marker='o')
plt.title("Average Fare by Month")
plt.xlabel("Month")
plt.ylabel("Average Fare ($)")
plt.grid()
plt.savefig(f"{output_dir}/monthly_avg_fare.png")
plt.close()