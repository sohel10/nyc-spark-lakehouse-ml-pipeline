-- Trip distribution
SELECT passenger_count, COUNT(*) AS trips
FROM taxi_data_test
GROUP BY passenger_count
ORDER BY passenger_count;

-- Avg fare (if column exists)
SELECT AVG(fare_amount) FROM taxi_data_test;