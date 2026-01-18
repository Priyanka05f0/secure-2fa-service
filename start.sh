#!/bin/bash
set -e

echo "Starting cron..."
cron

echo "Starting FastAPI server on port 8000..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
