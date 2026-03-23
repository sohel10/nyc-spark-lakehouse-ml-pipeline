CREATE TABLE new_trips (
    id SERIAL PRIMARY KEY,
    passenger_count INT,
    trip_distance FLOAT,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE model_monitoring (
    id SERIAL PRIMARY KEY,
    run_time TIMESTAMP,
    rmse FLOAT
);