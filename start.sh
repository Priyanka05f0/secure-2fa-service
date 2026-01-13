#!/bin/bash

echo "Starting cron service..."
service cron start

echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8080
