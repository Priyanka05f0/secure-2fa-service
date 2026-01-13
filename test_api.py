import requests
import os

# 1. Read the REAL encrypted seed from your file
with open("encrypted_seed.txt", "r") as f:
    real_seed_content = f.read().strip()

print(f"Read seed length: {len(real_seed_content)}")

# 2. Send it to your local Docker container
url = "http://localhost:8080/decrypt-seed"
payload = {"encrypted_seed": real_seed_content}

try:
    response = requests.post(url, json=payload)
    print("\n--- SERVER RESPONSE ---")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-----------------------\n")
    
    if response.status_code == 200:
        print("✅ SUCCESS! Your keys are working perfectly.")
    else:
        print("❌ FAILURE. Re-check if you rebuilt the container.")

except Exception as e:
    print(f"Connection Error: {e}")