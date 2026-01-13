import sys
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def generate_signature(commit_hash):
    print(f"🔒 Processing Commit Hash: {commit_hash}")

    # 1. Load Student Private Key
    try:
        with open("student_private.pem", "rb") as f:
            student_private = serialization.load_pem_private_key(f.read(), password=None)
    except FileNotFoundError:
        print("❌ Error: student_private.pem not found!")
        return

    # 2. Load Instructor Public Key
    try:
        with open("instructor_public.pem", "rb") as f:
            instructor_public = serialization.load_pem_public_key(f.read())
    except FileNotFoundError:
        print("❌ Error: instructor_public.pem not found!")
        return

    # 3. Sign the commit hash (RSA-PSS)
    signature = student_private.sign(
        commit_hash.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # 4. Encrypt the signature (RSA-OAEP)
    encrypted_signature = instructor_public.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 5. Base64 encode
    final_output = base64.b64encode(encrypted_signature).decode('utf-8')
    print("\n✅ GENERATION SUCCESSFUL")
    print("Copy the single line below for the 'Encrypted Commit Signature' field:")
    print("-" * 60)
    print(final_output)
    print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Usage: python sign_submission.py <YOUR_COMMIT_HASH>")
        print("Example: python sign_submission.py a1b2c3d4e5...")
    else:
        generate_signature(sys.argv[1])