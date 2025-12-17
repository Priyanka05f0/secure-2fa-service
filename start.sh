#!/bin/bash

# 1. Start the cron service
service cron start

# 2. Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8080