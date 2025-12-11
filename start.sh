#!/bin/bash

# 1. Start the cron service in the background
service cron start

# 2. Start the FastAPI server
# Host 0.0.0.0 is required for Docker
uvicorn main:app --host 0.0.0.0 --port 8080