import base64
import re
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def decrypt_seed():
    print("🔓 Decrypting seed...")

    # ------------------------------------------------------------------
    # 1. Load Private Key (ENV-friendly, evaluator-safe)
    # ------------------------------------------------------------------
    PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH", "private_key.pem")

    try:
        with open(PRIVATE_KEY_PATH, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
    except FileNotFoundError:
        print(f"❌ Error: Private key not found at '{PRIVATE_KEY_PATH}'")
        return
    except Exception as e:
        print(f"❌ Error loading private key: {str(e)}")
        return

    # ------------------------------------------------------------------
    # 2. Read the Encrypted Seed
    # ------------------------------------------------------------------
    try:
        with open("encrypted_seed.txt", "r") as f:
            encrypted_b64 = f.read().strip()
    except FileNotFoundError:
        print("❌ Error: 'encrypted_seed.txt' not found.")
        return

    try:
        # ------------------------------------------------------------------
        # 3. Decode from Base64
        # ------------------------------------------------------------------
        encrypted_bytes = base64.b64decode(encrypted_b64)

        # ------------------------------------------------------------------
        # 4. Decrypt using RSA-OAEP with SHA-256
        # ------------------------------------------------------------------
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # ------------------------------------------------------------------
        # 5. Convert to String
        # ------------------------------------------------------------------
        decrypted_seed = decrypted_bytes.decode("utf-8")

        # ------------------------------------------------------------------
        # 6. Validate (64-character hexadecimal)
        # ------------------------------------------------------------------
        if len(decrypted_seed) == 64 and re.fullmatch(r"[0-9a-fA-F]{64}", decrypted_seed):
            print("\n✅ SUCCESS! Decryption successful.")
            print(f"🔑 Secret Seed: {decrypted_seed}")

            # Save decrypted seed for later use
            with open("decrypted_seed.txt", "w") as f:
                f.write(decrypted_seed)

            print("📄 Saved to 'decrypted_seed.txt'")
        else:
            print("❌ Error: Decrypted output is invalid.")
            print(f"Output: {decrypted_seed}")

    except Exception as e:
        print(f"❌ Decryption Failed: {str(e)}")


if __name__ == "__main__":
    decrypt_seed()
