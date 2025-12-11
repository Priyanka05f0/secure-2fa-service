import base64
import re
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed():
    print("🔓 Decrypting seed...")

    # 1. Load your Private Key
    try:
        with open("student_private.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
    except FileNotFoundError:
        print("❌ Error: 'student_private.pem' not found.")
        return

    # 2. Read the Encrypted Seed
    try:
        with open("encrypted_seed.txt", "r") as f:
            encrypted_b64 = f.read().strip()
    except FileNotFoundError:
        print("❌ Error: 'encrypted_seed.txt' not found. Did Step 4 work?")
        return

    try:
        # 3. Decode from Base64
        encrypted_bytes = base64.b64decode(encrypted_b64)

        # 4. Decrypt using RSA-OAEP with SHA-256 (As per instructions)
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # 5. Convert to String
        decrypted_seed = decrypted_bytes.decode('utf-8')

        # 6. Validate (Must be 64 characters of Hexadecimal)
        if len(decrypted_seed) == 64 and re.fullmatch(r'^[0-9a-fA-F]+$', decrypted_seed):
            print("\n✅ SUCCESS! Decryption successful.")
            print(f"🔑 Your Secret Seed: {decrypted_seed}")
            
            # Save it to a file for later use
            with open("decrypted_seed.txt", "w") as f:
                f.write(decrypted_seed)
            print("📄 Saved to 'decrypted_seed.txt' (Keep this safe!)")
        else:
            print("❌ Error: Decryption produced invalid output (not a 64-char hex string).")
            print(f"Output: {decrypted_seed}")

    except Exception as e:
        print(f"❌ Decryption Failed: {str(e)}")

if __name__ == "__main__":
    decrypt_seed()