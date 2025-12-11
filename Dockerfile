# Use Python 3.9 slim version to keep it small
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# 1. Install system dependencies (Cron is required)
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# 2. Copy requirements and install Python libraries
# We create a requirements.txt on the fly to keep it simple for you
RUN echo "fastapi\nuvicorn\npydantic\ncryptography\npyotp\nrequests" > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy all your application files
COPY . .

# 4. Setup the Cron Job
# Runs cron_task.py every minute (*)
RUN echo "* * * * * root /usr/local/bin/python /app/cron_task.py >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron
RUN chmod 0644 /etc/cron.d/my-cron
RUN crontab /etc/cron.d/my-cron

# 5. Permissions for start script
RUN chmod +x /app/start.sh

# 6. Create volume directories so they exist
RUN mkdir -p /data /cron

# 7. Expose the port
EXPOSE 8080

# 8. Start the container
CMD ["/app/start.sh"]