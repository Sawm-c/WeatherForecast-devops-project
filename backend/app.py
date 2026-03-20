import os
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from datetime import datetime, timedelta

# --- THIẾT LẬP ĐƯỜNG DẪN ---
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))
frontend_dir = os.path.join(basedir, '..', 'frontend')

# Khởi tạo FastAPI
app = FastAPI(title="Weather API", description="API cho dự án Weather DevOps")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

images_dir = os.path.join(frontend_dir, 'images')
if os.path.exists(images_dir):
    app.mount("/images", StaticFiles(directory=images_dir), name="images")

# --- HÀM LOGIC ---
def get_dynamic_bg_url(data):
    condition = data['weather'][0]['main']
    
    now = data.get('dt')
    sunrise = data.get('sys', {}).get('sunrise')
    sunset = data.get('sys', {}).get('sunset')
    
    is_day = True
    if now and sunrise and sunset:
        is_day = sunrise <= now <= sunset

    if not is_day:
        return "/images/night.jpg"
    
    bg_map = {
        'Clear': "/images/clear.jpg",
        'Clouds': "/images/clouds.jpg",
        'Rain': "/images/rain.jpg",
        'Drizzle': "/images/drizzle.jpg",
        'Thunderstorm': "/images/thunder.jpg",
        'Fog': "/images/fog.jpg",
        'Mist': "/images/mist.jpg",
        'Haze': "/images/haze.jpg"
    }
    
    return bg_map.get(condition, "/images/clear.jpg")

def get_tomorrow_advice(t_data):
    w_ids = [w['id'] for item in t_data for w in item['weather']]
    temps = [item['main']['temp'] for item in t_data]
    winds = [item['wind']['speed'] for item in t_data]
    
    max_temp = max(temps)
    min_temp = min(temps)
    max_wind = max(winds)

   
    if any(200 <= id < 300 for id in w_ids): # Thunderstorm
        return "Warning: Thunderstorms expected. Stay indoors, avoid open spaces and water.", "text-white-500 font-bold"
    
    elif any(id in [502, 503, 504] for id in w_ids): # Heavy Rain 
        return "Alert: Heavy rain in the forecast. Watch out for localized flooding and drive safely.", "text-white-400 font-bold"
        
    elif any(600 <= id < 700 for id in w_ids): # Snow
        return "Snow is coming! Bundle up in warm layers, wear boots, and be careful of icy roads.", "text-white"
        
    elif max_temp >= 36: # Nắng nóng cực đoan
        return "Extreme heat warning! Stay hydrated, seek shade, and limit strenuous outdoor activities.", "text-white-500 font-bold"

    elif any(500 <= id <= 501 or id == 511 or 520 <= id <= 531 for id in w_ids): # Light/Moderate Rain
        return "Rain expected tomorrow. Don't forget your umbrella and a waterproof jacket.", "text-white-400"
        
    elif any(300 <= id < 400 for id in w_ids): # Drizzle
        return "Light drizzle expected. A light rain jacket or water-resistant windbreaker will be handy.", "text-white-300"
        
    elif any(700 <= id < 800 for id in w_ids): # Fog, Mist, Haze, Dust
        return "Visibility may be low due to fog, mist, or haze. Please drive slowly and keep a safe distance.", "text-white-300"
        
    elif max_wind >= 10: # Gió mạnh
        return "It's going to be a windy day. Secure loose items outdoors and wear a windbreaker.", "text-white-300"

    elif max_temp >= 30: # Trời nóng
        return "Hot and sunny day ahead! Remember to apply sunscreen, wear a hat, and drink plenty of water.", "text-white-400"
        
    elif min_temp <= 10: # Trời lạnh
        return "Chilly weather expected. A heavy coat, scarf, and gloves are recommended if you head out early.", "text-white-300"
        
    elif min_temp <= 18: # Trời mát mẻ/hơi lạnh
        return "Cool weather on the way. A sweater or light jacket will keep you comfortable.", "text-white-200"
        
    elif any(id == 800 for id in w_ids): # Trời trong xanh (Clear)
        return "Perfect weather! Clear skies and pleasant temperatures. A great day to be outdoors.", "text-white-300"
        
    else: # Mây mù hoặc các điều kiện bình thường khác
        return "Cloudy but stable weather expected. A comfortable day for most activities.", "text-white-200"


@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))

@app.get("/api/weather")
def get_weather(city: str):
    api_key = os.getenv('API_KEY')
    if not city or not api_key: 
        raise HTTPException(status_code=400, detail="Missing info or API Key")

    try:
        res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}")
        data = res.json()
        if res.status_code != 200: 
            raise HTTPException(status_code=res.status_code, detail=data)

        data['backgroundImage'] = get_dynamic_bg_url(data)

        f_res = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}")
        if f_res.status_code == 200:
            f_data = f_res.json().get('list', [])
            
            data['forecast'] = [{"time": i['dt_txt'].split(" ")[1][:5], "temp": round(i['main']['temp'], 1), "humidity": i['main']['humidity']} for i in f_data[:5]]

            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            t_data = [i for i in f_data if i['dt_txt'].startswith(tomorrow)] or f_data[8:16]
            
            summary, color = get_tomorrow_advice(t_data)
            data['summary'] = summary
            data['summary_color'] = color

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)