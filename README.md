
# 🌤️ Smart Weather Forecast & CI/CD Pipeline

A modern, containerized weather forecast web application built with FastAPI and Vanilla JavaScript. This project provides real-time weather tracking with a dynamic UI and showcases a complete DevOps lifecycle with automated CI/CD pipelines and Docker containerization.

[![CI/CD Pipeline](https://github.com/Sawm-c/WeatherForecast-devops-project/actions/workflows/main.yml/badge.svg)](https://github.com/Sawm-c/WeatherForecast-devops-project/actions/workflows/main.yml) ![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)

## ✨ Features
- **🌤️ Real-time Weather**: Accurate current weather conditions, AQI (Air Quality Index), and 5-hour forecasts.
- **🎨 Dynamic Interface**: Background images change dynamically based on the current weather condition (rain, clear, thunder, fog, etc.) and time of day.
- **💡 Smart Advice**: Intelligent recommendations based on temperature, humidity, and wind speed.
- **🐳 Containerized Environment**: Fully isolated multi-container setup using Docker and Docker Compose.
- **⚙️ Automated CI/CD**: Automated code linting and Docker image build/push processes triggered on every push to the main branch.
- **📱 Responsive Design**: Clean and modern glass-morphism UI built with Tailwind CSS.

## 🛠️ Tech Stack

### Backend
- **Python 3.11** - Core language
- **FastAPI** - High-performance web framework
- **Uvicorn** - ASGI web server
- **Requests** - HTTP library for external API calls

### Frontend
- **HTML5 & Vanilla JS** - Core structure and logic
- **Tailwind CSS** - Utility-first CSS framework (via CDN)
- **Google Fonts** - Poppins typography

### DevOps & Infrastructure
- **Docker & Docker Compose** - Containerization and orchestration
- **GitHub Actions** - CI/CD pipeline runner
- **Flake8** - Python code linter (PEP 8 compliance)
- **PostgreSQL 13** - Relational database 

## 🚀 Getting Started

### Prerequisites
- **Docker** and **Docker Compose** installed on your machine
- A valid API Key from [WeatherAPI](https://www.weatherapi.com/)
- **Git**

### Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/Sawm-c/WeatherForecast-devops-project.git
   cd WeatherForecast-devops-project

Configure Environment Variables
Create a .env file in the root directory and add your credentials:env# Database Configuration
DB_USER=postgres
DB_PASSW=your_secure_password
DB_NAME=weather_db

# Weather API
API_KEY=your_weatherapi_key_here
Start the application using Docker ComposeBashdocker-compose up -d --build
Open your browser
Navigate to http://localhost:8080 to see the weather app in action.

Local Development (Without Docker)
If you prefer to run the app directly using Python:
Bash# Install dependencies
pip install -r backend/requirements.txt

# Run the FastAPI server
python backend/app.py
Note: Ensure your .env file is properly set up before running locally.
📁 Project Structure
plaintext.
├── .github/workflows/   # GitHub Actions CI/CD configurations
│   └── main.yml         # Pipeline for testing and pushing Docker images
├── backend/             # Backend application code
│   ├── app.py           # Main FastAPI application and routing
│   └── requirements.txt # Python dependencies
├── database/            # Database initialization scripts
│   └── init.sql         # Table schemas and initial configurations
├── frontend/            # Frontend assets and interface
│   ├── images/          # Dynamic weather background images
│   └── index.html       # Main application UI
├── docker-compose.yml   # Multi-container orchestration config
├── Dockerfile           # Blueprint for the application image
├── .gitignore           # Ignored files and directories
└── README.md            # Project documentation
🔄 CI/CD Pipeline Architecture
This project implements a robust CI/CD pipeline using GitHub Actions. Every time code is pushed to the main branch, the following automated jobs are triggered:

Test-Code Job:
Sets up an Ubuntu runner with Python 3.11.
Installs dependencies.
Runs flake8 to enforce PEP 8 coding standards and catch syntax errors.

Build-and-Push Job:
Waits for the Test-Code job to pass successfully.
Securely logs into Docker Hub using GitHub Secrets.
Builds the Docker image and tags it with both latest and the dynamic Git commit SHA/tag.
Pushes the image to the Docker Hub registry.


🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

🙏 Acknowledgments

WeatherAPI: For providing accurate and comprehensive weather data.
Unsplash: For the beautiful weather background imagery.
Tailwind CSS: For making UI styling incredibly fast and efficient.

📞 Contact
Sawm-c - 💻 GitHub: @Sawm-c
⭐ Star this repository if you found it helpful or interesting!
