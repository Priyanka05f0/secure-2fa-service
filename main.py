from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import base64
import os
import re
import time
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pyotp

app = FastAPI()

# --- Configuration ---
DATA_DIR = "data"
# In Docker (later), this might be /data/seed.txt, but for now we use local folder
SEED_FILE = os.path.join(DATA_DIR, "seed.txt")
PRIVATE_KEY_FILE = "student_private.pem"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# --- Pydantic Models for Input Validation ---
class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

# --- Helper Function: Load Seed ---
def load_seed():
    if not os.path.exists(SEED_FILE):
        return None
    with open(SEED_FILE, "r") as f:
        return f.read().strip()

# --- Endpoint 1: Decrypt Seed ---
@app.post("/decrypt-seed")
def decrypt_seed(request: DecryptRequest):
    try:
        # 1. Load Private Key
        if not os.path.exists(PRIVATE_KEY_FILE):
            raise HTTPException(status_code=500, detail="Private key not found on server")
            
        with open(PRIVATE_KEY_FILE, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )

        # 2. Decode Base64 input
        encrypted_bytes = base64.b64decode(request.encrypted_seed)

        # 3. Decrypt using RSA-OAEP
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        decrypted_seed = decrypted_bytes.decode('utf-8')

        # 4. Validate (Must be 64-char hex)
        if len(decrypted_seed) != 64 or not re.fullmatch(r'^[0-9a-fA-F]+$', decrypted_seed):
             raise HTTPException(status_code=500, detail="Decryption produced invalid seed format")

        # 5. Save to File
        with open(SEED_FILE, "w") as f:
            f.write(decrypted_seed)

        return {"status": "ok"}

    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid base64 input")
    except Exception as e:
        # Catch-all for decryption failures
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

# --- Endpoint 2: Generate TOTP ---
@app.get("/generate-2fa")
def generate_2fa():
    seed = load_seed()
    if not seed:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    try:
        # Convert hex seed to base32 for pyotp
        seed_bytes = bytes.fromhex(seed)
        base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
        
        # Generate code
        totp = pyotp.TOTP(base32_seed)
        code = totp.now()
        
        # Calculate remaining validity time (30s window)
        remaining_seconds = 30 - int(time.time() % 30)
        
        return {
            "code": code,
            "valid_for": remaining_seconds
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

# --- Endpoint 3: Verify TOTP ---
@app.post("/verify-2fa")
def verify_2fa(request: VerifyRequest):
    if not request.code:
        raise HTTPException(status_code=400, detail="Missing code")
        
    seed = load_seed()
    if not seed:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    try:
        seed_bytes = bytes.fromhex(seed)
        base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
        
        totp = pyotp.TOTP(base32_seed)
        # Verify with +/- 1 period tolerance (30s)
        is_valid = totp.verify(request.code, valid_window=1)
        
        return {"valid": is_valid}
        
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Verification process failed: {str(e)}")

# --- Run Server (Only for debugging directly) ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)