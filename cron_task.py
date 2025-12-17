import time
import os
import datetime
import pyotp
import base64

# Define paths
SEED_FILE = "/data/seed.txt"
LOG_FILE = "/cron/last_code.txt"

def run_cron_job():
    if not os.path.exists(SEED_FILE):
        return

    try:
        with open(SEED_FILE, "r") as f:
            hex_seed = f.read().strip()

        seed_bytes = bytes.fromhex(hex_seed)
        base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
        totp = pyotp.TOTP(base32_seed)
        code = totp.now()

        utc_now = datetime.datetime.now(datetime.timezone.utc)
        timestamp = utc_now.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - 2FA Code: {code}\n"

        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_cron_job()