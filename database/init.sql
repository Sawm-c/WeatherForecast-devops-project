CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) UNIQUE NOT NULL, 
    weather_data JSONB NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE  INDEX idx_city_name_unique ON weather_data (LOWER(city_name));