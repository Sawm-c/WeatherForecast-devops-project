import os
import requests
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from dotenv import load_dotenv

# Xác định đúng đường dẫn thư mục
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '..', '.env')
load_dotenv(dotenv_path)

frontend_dir = os.path.join(basedir, '..', 'frontend')

app = Flask(__name__, static_folder=frontend_dir)
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City is required"}), 400
    
    api_key = os.getenv('API_KEY')
    if not api_key  :
        return jsonify({"error": "Missing API Key. Check .env file."}), 500

    try:
        # 1. Lấy dữ liệu Hiện tại
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}&lang=vi"
        response = requests.get(url)
        weather_data = response.json()

        if response.status_code != 200:
            return jsonify(weather_data), response.status_code

        # 2. Lấy dữ liệu Dự báo (Forecast)
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}&lang=vi"
        forecast_res = requests.get(forecast_url)
        
        forecast_list = []
        f_data = []
        if forecast_res.status_code == 200:
            f_data = forecast_res.json().get('list', [])
            for item in f_data[:5]:
                forecast_list.append({
                    "time": item['dt_txt'].split(" ")[1][:5],
                    "temp": round(item['main']['temp'], 1),
                    "humidity": item['main']['humidity']
                })
        
        # 3. Phân tích dữ liệu đưa ra Cảnh báo thông minh
        summary = "Thời tiết khá ổn định trong vài giờ tới."
        summary_color = "text-green-400" # Màu mặc định (Xanh lá)
        
        if forecast_list:
            all_temps = [item['temp'] for item in forecast_list]
            
            # Quét xem trong 24h tới (8 mốc x 3h) có mưa không
            has_rain = any(
                weather['main'] in ['Rain', 'Drizzle', 'Thunderstorm'] 
                for item in f_data[:8] for weather in item.get('weather', [])
            )
            
            if has_rain:
                summary = "Sắp có mưa, bạn nhớ mang theo ô nhé!"
                summary_color = "text-blue-300" # Đổi sang xanh dương
            elif max(all_temps) >= 35:
                summary = "Nắng nóng gay gắt, hãy chú ý bù nước và tránh nắng."
                summary_color = "text-red-400" # Đổi sang đỏ
            elif min(all_temps) <= 15:
                summary = "Trời sắp chuyển lạnh sâu, hãy giữ ấm cơ thể."
                summary_color = "text-cyan-300" # Đổi sang xanh lơ
            elif max(all_temps) - min(all_temps) >= 10:
                summary = "Nhiệt độ thay đổi đột ngột, cẩn thận cảm lạnh."
                summary_color = "text-yellow-400" # Đổi sang vàng

        weather_data['forecast'] = forecast_list
        weather_data['summary'] = summary
        weather_data['summary_color'] = summary_color
        
        return jsonify(weather_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)