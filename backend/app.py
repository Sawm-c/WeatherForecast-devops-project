import os
import random
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# ==============================
# THIẾT LẬP ĐƯỜNG DẪN & ENV
# ==============================
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))
API_KEY = os.getenv("API_KEY")
print(f"--- DEBUG: Key hiện tại là: [{API_KEY}] ---")

# ==============================
# KHỞI TẠO APP & LOAD ẢNH
# ==============================
app = FastAPI(title="Weather API", description="API cho dự án Weather DevOps")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cấu hình đường dẫn Frontend & Ảnh nền
frontend_dir = os.path.join(basedir, '..', 'frontend')
images_dir = os.path.join(frontend_dir, 'images')
if os.path.exists(images_dir):
    app.mount("/images", StaticFiles(directory=images_dir), name="images")

# ==============================
# ICON MAP
# ==============================
ICON_MAP = {
    "sunny": "☀️",
    "clear": "☀️",
    "partly cloudy": "⛅",
    "cloudy": "☁️",
    "overcast": "☁️",
    "mist": "🌫️",
    "fog": "🌫️",
    "haze": "🌫️",
    "light rain": "🌦️",
    "moderate rain": "🌧️",
    "heavy rain": "🌧️",
    "patchy rain": "🌦️",
    "thunder": "⛈️",
    "snow": "❄️"
}


def get_icon(condition):
    condition = condition.lower()
    for key in ICON_MAP:
        if key in condition:
            return ICON_MAP[key]
    return "🌤️"


# ==============================
# BACKGROUND LOGIC
# ==============================
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
            "/images/fog.jpg",
            "/images/mist.jpg",
            "/images/haze.jpg"
        ])

    if "cloud" in condition:
        return "/images/clouds.jpg"

    if "clear" in condition or "sunny" in condition:
        return random.choice([
            "/images/clear.jpg",
            "/images/clear2.jpg"
        ])

    return "/images/clear.jpg"


# ==============================
# FEELS LIKE ADVICE
# ==============================
def get_feels_like_advice(temp, humidity):
    if temp >= 30 and humidity >= 70:
        return "High humidity makes it feel hotter than actual temperature."
    if humidity >= 85:
        return "Very humid weather. You may feel uncomfortable."
    if humidity <= 40:
        return "Dry air. Stay hydrated."
    return ""


# ==============================
# SMART WEATHER ADVICE
# ==============================
def get_advice(forecast):
    conditions = [f["condition"].lower() for f in forecast]
    max_temp = max([f['temp'] for f in forecast])
    min_temp = min([f['temp'] for f in forecast])
    max_rain = max([f['rain'] for f in forecast])
    max_wind = max([f['wind'] for f in forecast])

    if any("thunder" in c for c in conditions):
        return "Thunderstorms expected. Stay indoors.", 
    "text-white-300 font-bold"

    if any("snow" in c for c in conditions):
        return "Snow expected. Keep warm and be careful.", "text-white-200"

    if max_rain > 80:
        return "Heavy rain expected. Risk of flooding.", 
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


# ==============================
# ROUTE TRANG CHỦ (FRONTEND)
# ==============================
@app.get("/")
async def read_index():
    # Hiển thị file HTML khi vào http://localhost:8080/
    return FileResponse(os.path.join(frontend_dir, 'index.html'))


# ==============================
# ROUTE LẤY DỮ LIỆU (API)
# ==============================
@app.get("/api/weather")
def get_weather(city: str):
    # Cấp dữ liệu JSON
    if not city:
        raise HTTPException(status_code=400, detail="City required")

    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API Key not found in environment variables"
        )

    url = (
        f"https://api.weatherapi.com/v1/forecast.json"
        f"?key={API_KEY}&q={city}&days=2&aqi=yes&alerts=yes"
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

        # Tính toán Timezone Offset chuẩn cho Frontend
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

        # ===== XỬ LÝ CHỈ SỐ KHÔNG KHÍ (AQI) =====
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

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=80, reload=True)
