import os
import requests
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder='public')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City is required"}), 400
    # Here you would normally call an external API to get the weather data
    # For demonstration purposes, we'll return a mock response
    api_key = os.getenv('API_KEY')

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}&lang=vi"
    response = requests.get(url)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Could not fetch weather data'}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
