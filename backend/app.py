import os
import json
import random
import requests
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles

# Setup paths and env variables
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))
API_KEY = os.getenv("API_KEY")

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSW = os.getenv("DB_PASSW", "postgres")
DB_NAME = os.getenv("DB_NAME", "weather_db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSW}@{DB_HOST}:5432/{DB_NAME}"
)


def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL, connect_timeout=3)
    except Exception as e:
        print(f"--- DB Error: {e} ---")
        return None


# Initialize FastAPI app and static files
app = FastAPI(title="Weather API", description="API for Weather DevOps")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = os.path.join(basedir, '..', 'frontend')
images_dir = os.path.join(frontend_dir, 'images')
if os.path.exists(images_dir):
    app.mount("/images", StaticFiles(directory=images_dir), name="images")

# Weather icon mapping
ICON_MAP = {
    "sunny": "☀️", "clear": "☀️", "partly cloudy": "⛅",
    "cloudy": "☁️", "overcast": "☁️", "mist": "🌫️",
    "fog": "🌫️", "haze": "🌫️", "light rain": "🌦️",
    "moderate rain": "🌧️", "heavy rain": "🌧️",
    "patchy rain": "🌦️", "thunder": "⛈️", "snow": "❄️"
}


def get_icon(condition):
    condition = condition.lower()
    for key in ICON_MAP:
        if key in condition:
            return ICON_MAP[key]
    return "🌤️"


# Dynamic background selection
def get_dynamic_bg(condition, is_day, rain):
    condition = condition.lower()

    if not is_day:
        return "/images/night.jpg"
    if "thunder" in condition:
        return "/images/thunder.jpg"
    if rain > 70:
        return "/images/rain.jpg"
    if rain > 30:
        return "/images/drizzle.jpg"
    if any(x in condition for x in ["fog", "mist", "haze"]):
        return random.choice([
            "/images/fog.jpg", "/images/mist.jpg", "/images/haze.jpg"
        ])
    if "cloud" in condition:
        return "/images/clouds.jpg"
    if "clear" in condition or "sunny" in condition:
        return random.choice(["/images/clear.jpg", "/images/clear2.jpg"])

    return "/images/clear.jpg"


# Feels-like temperature advice
def get_feels_like_advice(temp, humidity):
    if temp >= 30 and humidity >= 70:
        return "High humidity makes it feel hotter than actual temperature."
    if humidity >= 85:
        return "Very humid weather. You may feel uncomfortable."
    if humidity <= 40:
        return "Dry air. Stay hydrated."
    return ""


# Smart weather summary and advice
def get_advice(forecast):
    conditions = [f["condition"].lower() for f in forecast]
    max_temp = max([f['temp'] for f in forecast])
    min_temp = min([f['temp'] for f in forecast])
    max_rain = max([f['rain'] for f in forecast])
    max_wind = max([f['wind'] for f in forecast])

    if any("thunder" in c for c in conditions):
        return "Thunderstorms expected. Stay indoors.", \
               "text-white-300 font-bold"
    if any("snow" in c for c in conditions):
        return "Snow expected. Keep warm and be careful.", "text-white-200"
    if max_rain > 80:
        return "Heavy rain expected. Risk of flooding.", \
               "text-white-300 font-bold"
    if max_rain > 50:
        return "Moderate rain expected. Bring umbrella.", "text-white-300"
    if max_rain > 20:
        return "Light rain possible.", "text-blue-200"
    if any(x in c for c in conditions for x in ["fog", "mist", "haze"]):
        return "Low visibility due to fog or haze.", "text-white-300"
    if max_wind > 12:
        return "Strong winds expected.", "text-white-200"
    if max_temp >= 36:
        return "Extreme heat. Stay hydrated.", "text-white-300 font-bold"
    if max_temp >= 30:
        return "Hot weather. Wear sunscreen.", "text-white-300"
    if min_temp <= 10:
        return "Cold weather. Wear warm clothes.", "text-white-200"
    if min_temp <= 18:
        return "Cool weather. Light jacket recommended.", "text-white-200"
    if all("sunny" in c or "clear" in c for c in conditions):
        return "Perfect weather for outdoor activities!", "text-white-200"
    if any("cloud" in c for c in conditions):
        return "Cloudy but stable weather.", "text-white-200"

    return "Weather looks normal.", "text-white"


# Frontend route
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Weather Backend is running healthy"}


# Weather API route
@app.get("/api/weather")
def get_weather(city: str):
    if not city:
        raise HTTPException(status_code=400, detail="City required")

    # Normalize city name
    city_normalized = city.lower().strip()

    # 1. Check database cache
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT weather_data, updated_at "
                    "FROM weather_data WHERE city_name = %s",
                    (city_normalized,)
                )
                record = cur.fetchone()
                if record:
                    weather_data, updated_at = record
                    time_diff = datetime.now() - updated_at
                    # Return cache if updated within 30 minutes
                    if time_diff < timedelta(minutes=30):
                        print(f"--- CACHE HIT: {city_normalized} ---")
                        if isinstance(weather_data, str):
                            return json.loads(weather_data)
                        return weather_data
        except Exception as e:
            print(f"Cache Read Error: {e}")
        finally:
            conn.close()

    # 2. Fetch from WeatherAPI if no cache or expired
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API Key not found in environment variables"
        )

    url = (
        f"https://api.weatherapi.com/v1/forecast.json"
        f"?key={API_KEY}&q={city_normalized}&days=2&aqi=yes&alerts=yes"
    )

    try:
        res = requests.get(url)
        data = res.json()

        if res.status_code != 200:
            raise HTTPException(status_code=400, detail=data)

        current = data["current"]
        location = data["location"]
        condition_text = current["condition"]["text"]
        current_epoch = current["last_updated_epoch"]

        fc_day = data["forecast"]["forecastday"]
        all_hours = fc_day[0]["hour"] + fc_day[1]["hour"]
        future_hours = [
            h for h in all_hours if h["time_epoch"] > current_epoch
        ]

        forecast = []
        for h in future_hours[:5]:
            forecast.append({
                "time": h["time"].split(" ")[1],
                "temp": round(h["temp_c"], 1),
                "humidity": h["humidity"],
                "rain": h["chance_of_rain"],
                "wind": h["wind_kph"] / 3.6,
                "condition": h["condition"]["text"]
            })

        local_time_str = location["localtime"]
        local_time_dt = datetime.strptime(local_time_str, "%Y-%m-%d %H:%M")
        utc_time_dt = datetime.utcnow()

        offset_seconds = int((local_time_dt - utc_time_dt).total_seconds())
        timezone_offset_seconds = round(offset_seconds / 1800) * 1800

        response = {
            "name": location["name"],
            "sys": {"country": location["country"]},
            "timezone": timezone_offset_seconds,
            "main": {
                "temp": current["temp_c"],
                "feels_like": current["feelslike_c"],
                "humidity": current["humidity"],
                "pressure": current["pressure_mb"]
            },
            "weather": [{
                "main": condition_text,
                "description": condition_text
            }],
            "clouds": {"all": current["cloud"]},
            "wind": {"speed": current["wind_kph"] / 3.6},
            "visibility": current["vis_km"] * 1000,
        }

        response["icon"] = get_icon(condition_text)
        response["backgroundImage"] = get_dynamic_bg(
            condition_text,
            current["is_day"],
            forecast[0]["rain"] if forecast else 0
        )
        response["forecast"] = forecast
        summary, color = get_advice(forecast)
        response["summary"] = summary
        response["summary_color"] = color
        response["feels_advice"] = get_feels_like_advice(
            current["temp_c"],
            current["humidity"]
        )

        air_quality = current.get("air_quality", {})
        epa_index = air_quality.get("us-epa-index", 1)
        pm25 = round(air_quality.get("pm2_5", 0), 1)

        aqi_status = "Good"
        aqi_color = "text-green-400"

        if epa_index == 2:
            aqi_status = "Moderate"
            aqi_color = "text-yellow-400"
        elif epa_index == 3:
            aqi_status = "Unhealthy (Sensitive)"
            aqi_color = "text-orange-400"
        elif epa_index == 4:
            aqi_status = "Unhealthy"
            aqi_color = "text-red-400"
        elif epa_index == 5:
            aqi_status = "Very Unhealthy"
            aqi_color = "text-purple-400"
        elif epa_index == 6:
            aqi_status = "Hazardous"
            aqi_color = "text-rose-500 font-bold"

        response["aqi"] = {
            "status": aqi_status,
            "color": aqi_color,
            "pm25": pm25
        }

        # 3. Upsert new data to cache
        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    upsert_sql = """
                        INSERT INTO weather_data
                        (city_name, weather_data, updated_at)
                        VALUES (%s, %s, CURRENT_TIMESTAMP)
                        ON CONFLICT (city_name)
                        DO UPDATE SET
                            weather_data = EXCLUDED.weather_data,
                            updated_at = CURRENT_TIMESTAMP;
                    """
                    cur.execute(
                        upsert_sql,
                        (city_normalized, json.dumps(response))
                    )
                    conn.commit()
                    print(f"--- CACHE UPSERTED: {city_normalized} ---")
            except Exception as e:
                print(f"Cache Write Error: {e}")
            finally:
                conn.close()

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=80, reload=True)
