import pyotp
import base64
import time

# Function 1: Generate the TOTP Code
def generate_totp_code(hex_seed: str) -> str:
    # 1. Convert hex seed to bytes
    seed_bytes = bytes.fromhex(hex_seed)
    
    # 2. Convert bytes to base32 (Required by TOTP libraries)
    # pyotp requires a base32 string as the secret
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    
    # 3. Create TOTP object
    # Default is already SHA-1, 6 digits, 30s interval
    totp = pyotp.TOTP(base32_seed)
    
    # 4. Generate current code
    return totp.now()

# Function 2: Verify the Code
def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    # 1. Convert hex seed to base32 (same as above)
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    
    # 2. Create TOTP object
    totp = pyotp.TOTP(base32_seed)
    
    # 3. Verify with window
    # valid_window=1 means it checks current time, +30s ahead, and -30s behind
    return totp.verify(code, valid_window=valid_window)

# --- Test Block (Runs only when you run this file directly) ---
if __name__ == "__main__":
    try:
        # Load the decrypted seed from the file we made in Step 5
        with open("decrypted_seed.txt", "r") as f:
            my_seed = f.read().strip()
            
        print(f"Loaded Seed: {my_seed[:10]}... (hidden)")
        
        # Generate a code
        code = generate_totp_code(my_seed)
        print(f"Generated Code: {code}")
        
        # Verify it immediately
        is_valid = verify_totp_code(my_seed, code)
        print(f"Verification Result: {is_valid}")
        
    except FileNotFoundError:
        print("❌ Error: Could not find 'decrypted_seed.txt'. Did you finish Step 5?")