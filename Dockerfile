# Use Python 3.9 slim
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# 1. Install system dependencies (Cron is required)
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# 2. Install Python libraries
RUN echo "fastapi\nuvicorn\npydantic\ncryptography\npyotp\nrequests" > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy all application files
COPY . .

# 4. Setup the Cron Job
RUN echo "* * * * * root /usr/local/bin/python /app/cron_task.py >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron
RUN chmod 0644 /etc/cron.d/my-cron
RUN crontab /etc/cron.d/my-cron

# 5. [CRITICAL FIX] Fix Windows line endings in start.sh and make executable
RUN sed -i 's/\r$//' /app/start.sh && chmod +x /app/start.sh

# 6. Create volume directories
RUN mkdir -p /data /cron

# 7. Expose the port
EXPOSE 8000

# 8. Start the container
CMD ["bash", "start.sh"]