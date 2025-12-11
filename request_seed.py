import requests
import json
import sys

# --- CONFIGURATION ---
# REPLACE THIS with your actual Student ID!
STUDENT_ID = "23MH1A05F0" 

# Your Repo URL
GITHUB_REPO_URL = "https://github.com/Priyanka05f0/secure-2fa-service"

# The API Endpoint
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def get_encrypted_seed():
    print(f"🚀 Requesting seed for Student ID: {STUDENT_ID}")
    
    # 1. Read your public key
    try:
        with open("student_public.pem", "r") as f:
            public_key_content = f.read()
    except FileNotFoundError:
        print("❌ Error: student_public.pem not found.")
        return

    # 2. Prepare the data payload
    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": public_key_content
    }

    # 3. Send POST request
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "encrypted_seed" in data:
                seed_content = data["encrypted_seed"]
                # 4. Save to file
                with open("encrypted_seed.txt", "w") as f:
                    f.write(seed_content)
                print("✅ SUCCESS: Encrypted seed saved to 'encrypted_seed.txt'")
            else:
                print("⚠️  Warning: API returned 200 but no seed found.")
                print(data)
        else:
            print(f"❌ Failed with Status Code: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    # Safety check
    if STUDENT_ID == "YOUR_STUDENT_ID_HERE":
        print("❌ STOP: You forgot to put in your Student ID in the script!")
    else:
        # Install requests if you haven't yet
        # pip install requests
        get_encrypted_seed()