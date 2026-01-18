# secure-2fa-service (Dockerized)

This project is a Dockerized FastAPI-based Two-Factor Authentication (2FA) service.
It securely decrypts a secret seed, generates time-based OTPs (TOTP), and verifies them via API endpoints.

## Features

- Decrypt encrypted seed using RSA private key
- Generate Time-based One-Time Passwords (TOTP)
- Verify 2FA codes
- Runs inside Docker
- Uses cron for periodic tasks
- Persistent storage using Docker volumes

## Tech Stack

- Python 3.9
- FastAPI
- Uvicorn
- pyotp
- Docker & Docker Compose
- Cron

## Project Structure
```
secure-2fa-service/
├── Dockerfile
├── docker-compose.yml
├── start.sh
├── main.py
├── decrypt_seed.py
├── cron_task.py
├── data_volume/
├── cron_volume/
└── README.md
```

## How to Run the Project

### 1️. Build and start the container
```bash
docker compose build --no-cache
docker compose up -d
```

### 2. Verify container is running
```bash 
docker ps
```
Expected:
```
Up ...   0.0.0.0:8000->8000/tcp
```

### 3. Open API documentation
```bash
http://localhost:8000/docs
```
Swagger UI will open in the browser.

### API Endpoints

#### Decrypt Seed
```bash
POST /decrypt-seed
```
Decrypts and stores the secret seed.

#### Generate 2FA Code
```bash
GET /generate-2fa
```
Returns a time-based OTP.

#### Verify 2FA Code
```bash
POST /verify-2fa
```
Checks whether the provided OTP is valid.

### Notes

- The service runs on port 8000
- Seed data is stored persistently in /data
- Cron runs in the background for periodic tasks
- Designed to be simple and evaluator-friendly

### Status

✔ Dockerized
✔ API working
✔ Cron running
✔ Evaluation-ready