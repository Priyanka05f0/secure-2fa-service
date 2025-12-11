import time
import os
import datetime
import pyotp
import base64

# Define paths (As per Docker instructions)
SEED_FILE = "/data/seed.txt"
LOG_FILE = "/cron/last_code.txt"

def run_cron_job():
    # 1. Check if seed exists
    if not os.path.exists(SEED_FILE):
        print(f"[{datetime.datetime.now()}] Seed not found yet.")
        return

    try:
        # 2. Read the seed
        with open(SEED_FILE, "r") as f:
            hex_seed = f.read().strip()

        # 3. Generate TOTP
        seed_bytes = bytes.fromhex(hex_seed)
        base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
        totp = pyotp.TOTP(base32_seed)
        code = totp.now()

        # 4. Format the log entry
        # Format: YYYY-MM-DD HH:MM:SS - 2FA Code: XXXXXX
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        timestamp = utc_now.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - 2FA Code: {code}\n"

        # 5. Append to log file
        # Ensure directory exists
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
            
        print(f"Logged: {log_entry.strip()}")

    except Exception as e:
        print(f"Error in cron job: {e}")

if __name__ == "__main__":
    run_cron_job()