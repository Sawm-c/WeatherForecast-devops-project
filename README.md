# 🌤️ WeatherForecast DevOps Project

A production-ready weather forecasting web application built with a modern **DevOps stack** — fully automated from code to cloud.

> **Live Demo:** [http://\<EC2_IP\>](http://localhost) | **GitHub Actions:** See [CI/CD Pipeline](.github/workflows/main.yml)

---

## 📐 Architecture Overview

```
                         ┌─────────────────────────────────────────────────┐
                         │                  AWS Cloud                       │
                         │                                                  │
  User Browser           │    ┌──────────────────────────────────────────┐  │
      │                  │    │             VPC (10.0.0.0/16)            │  │
      │  HTTP :80        │    │                                          │  │
      ▼                  │    │  ┌─────────────────────────────────────┐ │  │
 ┌─────────┐  EIP  ──────┼────┼─▶│          EC2 (t2.micro)            │ │  │
 │ Internet│             │    │  │                                     │ │  │
 └─────────┘             │    │  │  ┌──────────┐    ┌─────────────┐   │ │  │
                         │    │  │  │  Nginx   │───▶│  FastAPI    │   │ │  │
                         │    │  │  │(Frontend)│    │  (Backend)  │   │ │  │
                         │    │  │  └──────────┘    └──────┬──────┘   │ │  │
                         │    │  │                         │          │ │  │
                         │    │  │                  ┌──────▼──────┐   │ │  │
                         │    │  │                  │  PostgreSQL  │   │ │  │
                         │    │  │                  │     (DB)     │   │ │  │
                         │    │  │                  └─────────────┘   │ │  │
                         │    │  └─────────────────────────────────────┘ │  │
                         │    │                                          │  │
                         │    │  ┌──────────┐  ┌──────────┐             │  │
                         │    │  │    S3    │  │   IAM    │             │  │
                         │    │  │ (Storage)│  │  (Role)  │             │  │
                         │    │  └──────────┘  └──────────┘             │  │
                         │    └──────────────────────────────────────────┘  │
                         └─────────────────────────────────────────────────┘
```

---

## 🔄 CI/CD Pipeline

```
  Push to main
       │
       ▼
  ┌─────────┐     ┌──────────────────────┐     ┌────────────────────────┐
  │  Test   │────▶│   Build & Push       │────▶│   Deploy to EC2        │
  │         │     │                      │     │                        │
  │ flake8  │     │ Docker build backend │     │ SSH into server        │
  │ lint    │     │ Docker build frontend│     │ git pull               │
  └─────────┘     │ Push to Docker Hub   │     │ docker compose pull    │
                  └──────────────────────┘     │ docker compose up -d   │
                                               └────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer                | Technology                                 |
| -------------------- | ------------------------------------------ |
| **Frontend**         | HTML, CSS (TailwindCSS), JavaScript, Nginx |
| **Backend**          | Python, FastAPI, Uvicorn                   |
| **Database**         | PostgreSQL 13                              |
| **Containerization** | Docker, Docker Compose                     |
| **CI/CD**            | GitHub Actions                             |
| **Infrastructure**   | Terraform (IaC)                            |
| **Cloud**            | AWS (EC2, S3, VPC, IAM, EIP)               |
| **Registry**         | Docker Hub                                 |

---

## 🗂️ Project Structure

```
WeatherForecast-devops-project/
├── .github/
│   └── workflows/
│       └── main.yml          # CI/CD Pipeline
├── backend/
│   ├── app.py                # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html            # Weather Dashboard UI
│   ├── nginx.conf            # Reverse proxy config
│   └── Dockerfile
├── database/
│   └── init.sql              # DB initialization script
├── terraform/
│   ├── main.tf               # Root module
│   ├── variable.tf
│   ├── terraform.tfvars
│   ├── output.tf
│   └── modules/
│       ├── network/          # VPC, Subnets, NAT Gateway
│       ├── security/         # Security Groups
│       ├── iam/              # IAM Roles & Policies
│       ├── storage/          # S3 Bucket
│       └── app/              # EC2 Instance, EIP
└── docker-compose.yml
```

---

## ✨ Key Features

- **3-Tier Architecture:** Nginx (FE) → FastAPI (BE) → PostgreSQL (DB), all containerized.
- **Reverse Proxy:** Nginx routes `/api/*` requests to FastAPI internally — no exposed backend ports.
- **Weather Caching:** API responses cached in PostgreSQL for 30 minutes to reduce external API calls.
- **Fully Automated CI/CD:** Every push to `main` triggers build, test, and deployment automatically.
- **Infrastructure as Code:** Entire AWS infrastructure defined and reproducible via Terraform modules.
- **Least-Privilege IAM:** EC2 has only the permissions it needs to read from S3.
- **Private Networking:** Database is not exposed to the internet; only accessible within the VPC.

---

## 🚀 How to Deploy

### Prerequisites

- AWS CLI configured
- Terraform >= 1.0
- SSH key pair generated

### 1. Provision Infrastructure

```bash
cd terraform
terraform init
terraform apply
```

### 2. Configure GitHub Secrets

| Secret               | Description                            |
| -------------------- | -------------------------------------- |
| `DOCKERHUB_USERNAME` | Docker Hub username                    |
| `DOCKERHUB_TOKEN`    | Docker Hub access token                |
| `SV_IP`              | EC2 Elastic IP (from Terraform output) |
| `SV_USER`            | EC2 username (`ec2-user`)              |
| `WF_PRV_KEY`         | SSH private key content                |
| `DB_USER`            | PostgreSQL username                    |
| `DB_PASSW`           | PostgreSQL password                    |
| `DB_NAME`            | PostgreSQL database name               |
| `API_KEY`            | WeatherAPI.com API key                 |

### 3. Push to Deploy

```bash
git push origin main
# GitHub Actions will automatically build, push images, and deploy to EC2
```

---

## 🌐 API Endpoints

| Method | Endpoint                   | Description                 |
| ------ | -------------------------- | --------------------------- |
| `GET`  | `/`                        | Weather Dashboard UI        |
| `GET`  | `/api/weather?city={city}` | Get weather data for a city |

---

## 💡 What I Learned

- Designing a **modular Terraform** infrastructure with reusable components.
- Implementing a **3-tier containerized** application with Docker Compose.
- Configuring **Nginx as a reverse proxy** to route traffic between services.
- Building a complete **CI/CD pipeline** with GitHub Actions for automated deployments.
- Applying **AWS security best practices** (Security Groups, IAM least-privilege, private subnets).
- Managing **infrastructure state** and resolving Terraform state lock issues.

---

## 📸 Screenshots

> _(Add screenshots of the running app, GitHub Actions pipeline, and AWS Console here)_

---

## 📄 License

MIT License — feel free to use this project as a reference.
 
 
