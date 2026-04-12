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
- **Docker & Docker Compose V2** - Containerization and orchestration
- **GitHub Actions** - CI/CD pipeline runner
- **Terraform** - Infrastructure as Code (IaC) to provision AWS EC2
- **AWS EC2** - Production hosting environment
- **Nginx** - Web server and reverse proxy
- **Flake8** - Python code linter (PEP 8 compliance)
- **PostgreSQL 13** - Relational database 

## 🚀 Getting Started

### Prerequisites
- **Docker** and **Docker Compose** installed on your machine
- A valid API Key from [WeatherAPI](https://www.weatherapi.com/)
- **Git**

### Installation
1. **Clone the repository**
   git clone https://github.com/Sawm-c/WeatherForecast-devops-project.git
   cd WeatherForecast-devops-project

2. **Configure Environment Variables**
   ```Markdown
   Create a .env file in the root directory and add your credentials:
   
   # Database Configuration
   DB_USER=postgres
   DB_PASSW=your_secure_password
   DB_NAME=weather_db
   
   # Weather API
   API_KEY=your_weatherapi_key_here
   ```
3. **Start the application using Docker Compose V2**
   ```bash
   docker compose up -d --build

   Open your browser and navigate to `http://localhost:8080` to see the weather app in action.
   ```
4. **Local Development (Without Docker)**
   If you prefer to run the app directly using Python:
   ```bash
   # Install dependencies
   pip install -r backend/requirements.txt
   
   # Run the FastAPI server
   python backend/app.py
   ```
   *Note: Ensure your .env file is properly set up before running locally.*

## 📁 Project Structure
```
.
├── .github/workflows/   # GitHub Actions CI/CD pipeline configurations
│   └── main.yml         # Pipeline for testing, building, and deployment
├── backend/             # Backend application code
│   ├── app.py           # Main FastAPI application and routing
│   ├── Dockerfile       # Blueprint for the backend container
│   └── requirements.txt # Python dependencies
├── database/            # Database initialization scripts
│   └── init.sql         # Table schemas and initial configurations
├── frontend/            # Frontend assets and interface
│   ├── images/          # Dynamic weather background images
│   ├── index.html       # Main application UI
│   ├── Dockerfile       # Blueprint for the Nginx frontend container
│   └── nginx.conf       # Nginx reverse proxy configurations
├── terraform/           # Infrastructure as Code (IaC)
│   ├── main.tf          # AWS EC2 & Security Group provisioning
│   └── variable.tf      # Variables for Terraform
├── docker-compose.yml   # Multi-container orchestration config
├── .gitignore           # Ignored files and directories
└── README.md            # Project documentation
```

## 🔄 Architecture & CI/CD Pipeline

This project utilizes **Terraform** to automatically provision infrastructure on AWS (EC2 instance, Security Groups) and a robust CI/CD pipeline using GitHub Actions. Upon pushing to the main branch, the following automated jobs are triggered:

1. **Test Job (`test`):**
   - Sets up an Ubuntu runner with Python 3.11.
   - Installs dependencies.
   - Runs `flake8` to enforce PEP 8 coding standards and catch syntax errors in the backend code.

2. **Build and Push Job (`build-and-push`):**
   - Waits for the `test` job to pass successfully.
   - Securely logs into Docker Hub using GitHub Secrets.
   - Builds separate Docker images for the frontend (Nginx) and backend (FastAPI).
   - Tags and pushes both images to the Docker Hub registry.

3. **Deploy Job (`deploy`):**
   - Waits for the `build-and-push` job to complete.
   - Connects to the AWS EC2 instance strictly via SSH.
   - Pulls the latest system code and updates the `.env` file with secure repository secrets (including Docker Hub username).
   - Pulls the latest Docker images from Docker Hub and orchestrates the deployment using `docker compose`.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (git checkout -b feature/updtFeature)
3. Commit your changes (git commit -m 'Add some updtFeature')
4. Push to the branch (git push origin feature/updtFeature)
5. Open a Pull Request

## 🙏 Acknowledgments
- **WeatherAPI**: For providing accurate and comprehensive weather data.
- **Unsplash**: For the beautiful weather background imagery.
- **Tailwind CSS**: For making UI styling incredibly fast and efficient.

## 📞 Contact
Sawm-c - 💻 GitHub: @Sawm-c (https://github.com/Sawm-c)
📧 Email: hieuhc53@gmail.com

⭐ Star this repository if you found it helpful or interesting!
