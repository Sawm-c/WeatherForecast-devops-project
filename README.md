# 🌤️ WeatherForecast DevOps Project

A **production-grade, multi-tier serverless web application** that fetches real-time weather data, built end-to-end with a modern DevOps workflow.

The application serves a **static Frontend (S3 + CloudFront CDN)** backed by a **containerized FastAPI on EC2** connected to a **PostgreSQL database in a private subnet** — all accessible securely via a custom HTTPS domain. All 40+ cloud resources are provisioned automatically using **modular Terraform**. Every merge to `main` triggers a **4-stage GitHub Actions pipeline** — code quality check → Docker build & push → deploy Backend → sync Frontend to S3.

> **Live Demo:** [https://weather.chhieu.space](https://weather.chhieu.space)

> **Stack:** Python · FastAPI · PostgreSQL · Docker · Terraform · GitHub Actions · AWS (S3, CloudFront, EC2, VPC, IAM, ACM)

---

## 📐 Architecture Overview

```
                                        AWS Cloud (ap-southeast-1)
                                 ┌────────────────────────────────────────────────────────────┐
  Developer                      │                                                            │
      │ git push                 │                         ┌──────────────────────────────┐   │
      ▼                          │    S3 Bucket            │  VPC  10.0.0.0/16            │   │
  GitHub Actions ──────────────────► (Frontend Static) ◄───┤                              │   │
  (CI/CD Pipeline)               │                         │  Public Subnet               │   │
                                 │                         │  ┌──────────────────────┐    │   │
  User Browser                   │  ┌──────────────────┐   │  │ EC2 t3.micro (EIP)   │    │   │
      │ HTTPS                    │  │ CloudFront (CDN) │   │  │                      │    │   │
      └───────────────────────────► │ weather.chhieu.  │   │  │  Docker Container    │    │   │
                                 │  │ space            │   │  │  ┌────────────────┐  │    │   │
                                 │  │                  │───┼──┼─►│ FastAPI :80    │  │    │   │
                                 │  │ /api/* ──────────────┼──┘  └───────┬────────┘  │    │   │
                                 │  │ /*    → S3 Bucket│   │             │           │    │   │
                                 │  └──────────────────┘   │  Private Subnet         │    │   │
                                 │                         │  ┌──────────────────┐   │    │   │
                                 │  ┌───────────────────┐  │  │ EC2 (PostgreSQL) │◄──┘    │   │
                                 │  │ S3 (init.sql)─────┼──┼─►│  :5432           │        │   │
                                 │  │ VPC Gateway EP    │  │  └──────────────────┘        │   │
                                 │  └───────────────────┘  └──────────────────────────────┘   │
                                 └────────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

| Decision | Rationale |
| :--- | :--- |
| **CloudFront `/api/*` Proxy** | Routes API calls through CloudFront (HTTPS) to Backend EC2 (HTTP). Eliminates Mixed Content & CORS issues entirely — no SSL needed on EC2. |
| **Database in Private Subnet** | PostgreSQL EC2 has no public IP. Only reachable via Security Group from Backend EC2. Zero internet exposure. |
| **S3 VPC Gateway Endpoint** | Private Subnet DB can pull `init.sql` from S3 directly — no NAT Gateway needed, saving ~$32/month. |
| **OAC (not OAI) for S3** | Origin Access Control is the modern, recommended approach to prevent direct public S3 access. |
| **Elastic IP for Backend** | Keeps Backend IP stable across EC2 reboots, so CloudFront origin config never needs updating. |
| **No NAT Gateway** | Cost optimization: Backend is in a Public Subnet (with EIP) and DB uses S3 VPC Gateway Endpoint. NAT Gateway ($32+/month) completely eliminated. |

---

## 🔄 CI/CD Pipeline

Every **merge to `main`** triggers a **4-stage automated pipeline** with branch protection :

```
  Open Pull Request
         │
         ▼
  ┌─────────────┐
  │   Stage 1   │  ← Runs on every PR (Gate: must pass before merge is allowed)
  │    TEST     │
  │   flake8    │
  │  lint check │
  └──────┬──────┘
         │  (PR merged to main)
         ▼
  ┌─────────────┐     ┌───────────────────────────┐     ┌────────────────────────────────────────┐
  │   Stage 2   │     │         Stage 3           │     │               Stage 4                  │
  │  BUILD &    │────▶│      DEPLOY BACKEND       │     │           DEPLOY FRONTEND              │
  │  PUSH       │     │                           │     │                                        │
  │             │     │  SSH into Backend EC2     │     │  aws s3 sync ./frontend/ → S3 Bucket   │
  │  docker     │     │  git pull origin main     │     │  CloudFront cache invalidation (/*)    │
  │  build      │     │  Write .env from Secrets  │     │                                        │
  │  push to    │     │  docker compose pull      │     │  (Runs in parallel with Stage 3)       │
  │  Docker Hub │     │  docker compose up -d     │     │                                        │
  └─────────────┘     └───────────────────────────┘     └────────────────────────────────────────┘
```

> **Branch Protection Rule:** `main` branch is protected. Direct pushes are blocked. All changes must go through a Pull Request and CI must pass before merging.

---

## ☁️ Infrastructure as Code (Terraform)

Infrastructure is fully defined in **modular Terraform** — reproducible with a single `terraform apply`.

**40+ AWS resources provisioned automatically:**

| Module | Resources Created |
| :--- | :--- |
| `network` | VPC, Public/Private Subnets (3 AZs each), Internet Gateway, Route Tables, S3 VPC Gateway Endpoint |
| `security_be` | Backend Security Group (Port 80 from `0.0.0.0/0`, Port 22 for SSH) |
| `security_db` | Database Security Group (Port 5432 **only from Backend SG** — no public access) |
| `iam` | IAM Role, Policy (S3 read), Instance Profile (attached to both EC2s) |
| `storage` | S3 Bucket (stores `init.sql` for DB seeding) |
| `be` | Backend EC2 (Public Subnet), Elastic IP, Docker Compose via `user_data` |
| `database` | Database EC2 (Private Subnet), PostgreSQL 15, seeded from S3 via VPC Endpoint |
| `fe` | Frontend S3 Bucket (private), CloudFront OAC, CloudFront Distribution (multi-origin), S3 Bucket Policy, ACM SSL Certificate binding |

---

## 🛠️ Tech Stack

**Application**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**DevOps & Infrastructure**

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Amazon AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Docker Hub](https://img.shields.io/badge/Docker_Hub-2496ED?style=for-the-badge&logo=docker&logoColor=white)

---

## 🗂️ Project Structure

```
WeatherForecast-devops-project/
├── .github/
│   └── workflows/
│       └── main.yml              # CI/CD Pipeline: Test → Build → Deploy BE + Deploy FE
├── backend/
│   ├── app.py                    # FastAPI application & weather API integration
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── index.html                # Weather Dashboard UI (served from S3 + CloudFront)
├── database/
│   └── init.sql                  # PostgreSQL schema initialization (pulled from S3)
├── terraform/
│   ├── main.tf                   # Root module — orchestrates all child modules
│   ├── variable.tf               # All input variable declarations
│   ├── terraform.tfvars          # Actual values (gitignored for sensitive data)
│   ├── output.tf                 # Outputs: BE IP, DB Private IP, Frontend URL, etc.
│   └── modules/
│       ├── network/              # VPC, Subnets, IGW, Route Tables, S3 VPC Gateway Endpoint
│       ├── security_be/          # Backend Security Group (Port 80, 22)
│       ├── security_db/          # DB Security Group (Port 5432 from BE SG only)
│       ├── iam/                  # IAM Role, Policy & Instance Profile
│       ├── storage/              # S3 Bucket (for init.sql)
│       ├── be/                   # Backend EC2, Elastic IP
│       ├── database/             # DB EC2 (Private Subnet), PostgreSQL 15
│       └── fe/                   # S3 Frontend Bucket, CloudFront OAC + Distribution
├── docker-compose.yml            # Single-service Backend container orchestration
└── README.md
```

---

## ✨ Key Features

- **Multi-Origin CloudFront:** Routes `/api/*` to Backend EC2 and `/*` to S3 — eliminates Mixed Content & CORS entirely.
- **Serverless Frontend:** HTML/CSS/JS hosted on private S3, distributed globally via CloudFront CDN with HTTPS.
- **Custom Domain & SSL:** `weather.chhieu.space` with ACM Wildcard Certificate (`*.chhieu.space`), zero-downtime updates.
- **Isolated Private Database:** PostgreSQL EC2 has no public IP. Only reachable via Security Group from Backend EC2. DB seeded from S3 via VPC Gateway Endpoint — no NAT Gateway required.
- **Weather Caching:** API responses cached in PostgreSQL for 30 minutes to minimize external API calls.
- **Fully Automated CI/CD:** Merge to `main` triggers test → build → deploy — no manual steps.
- **Branch Protection:** Direct pushes to `main` blocked. All changes must pass CI (flake8) before merge.
- **Infrastructure as Code:** All 40+ AWS resources defined in modular, reusable Terraform modules with zero hardcoded values.
- **Least-Privilege IAM:** EC2 instances have only the minimum S3 permissions needed.

---

## 🚀 How to Deploy

### Prerequisites

- AWS CLI configured (`aws configure`)
- Terraform >= 1.0 installed
- SSH key pair generated
- ACM Certificate issued in `us-east-1` for your domain
- Domain DNS managed on your registrar (e.g., Spaceship, Namecheap)

### 1. Provision AWS Infrastructure

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
# Outputs: weather_be_ip, database_prv_ip, frontend_url, fe_bucket_name, cloudfront_distribution_id
```

### 2. Configure GitHub Secrets

Add these to **Settings → Secrets and variables → Actions** in your GitHub repo:

| Secret | Description |
| :--- | :--- |
| `SV_IP` | Backend EC2 Elastic IP (from Terraform output) |
| `SV_USER` | EC2 username (`ec2-user`) |
| `WF_PRV_KEY` | SSH private key content |
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `DB_PRIVATE_IP` | DB EC2 Private IP (from Terraform output) |
| `DB_USER` | PostgreSQL username |
| `DB_PASSW` | PostgreSQL password |
| `DB_NAME` | PostgreSQL database name |
| `API_KEY` | OpenWeatherMap API key |
| `FE_BUCKET_NAME` | Frontend S3 Bucket name (from Terraform output) |
| `CF_DISTRIBUTION_ID` | CloudFront Distribution ID (from Terraform output) |
| `AWS_REGION` | `ap-southeast-1` |
| `AWS_ACCESS_KEY_ID` | AWS IAM Access Key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM Secret Key |

### 3. Configure DNS on your Registrar

Add a CNAME record pointing your subdomain to CloudFront:

| Type | Host | Value |
| :--- | :--- | :--- |
| `CNAME` | `weather` | `<your-cloudfront-domain>.cloudfront.net` |

### 4. Push to Deploy

```bash
git checkout -b feature/my-changes
# ... make changes ...
git push origin feature/my-changes
# Open Pull Request → CI runs flake8 check
# Merge PR → Full pipeline: Build Docker → Deploy BE via SSH → Sync FE to S3 + Invalidate CloudFront Cache
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check — returns `{"status": "ok"}` |
| `GET` | `/api/weather?city={city}` | Fetch weather data for any city (cached 30 min in PostgreSQL) |

---

## 💡 What I Learned

- Designing **multi-origin CloudFront distributions** to proxy API requests — eliminating Mixed Content and CORS without SSL on the backend.
- Building **fully modular Terraform** infrastructure (40+ resources) with zero hardcoded values across 8 composable child modules.
- Securing a **PostgreSQL database in a Private Subnet** with Security Groups, seeded via **VPC S3 Gateway Endpoint** — no NAT Gateway required.
- Implementing **GitOps best practices**: Branch Protection Rules with required CI status checks, preventing any code from reaching `main` without passing tests.
- Configuring **ACM Wildcard SSL Certificates** with DNS validation and binding them to CloudFront distributions via Terraform.
- Applying **AWS security best practices**: OAC for S3, least-privilege IAM, private subnets, Security Group chaining.

---

## 📄 License

MIT License — feel free to use this project as a reference.
