import sys
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# 1. Get the commit hash from command line
if len(sys.argv) < 2:
    print("Error: Please provide your commit hash")
    print("Usage: python sign_submission.py <YOUR_COMMIT_HASH>")
    sys.exit(1)

commit_hash = sys.argv[1]

# 2. Load Your Private Key
try:
    with open("student_private.pem", "rb") as f:
        student_private_key = serialization.load_pem_private_key(f.read(), password=None)
except FileNotFoundError:
    print("Error: 'student_private.pem' not found. Make sure you are in the correct folder.")
    sys.exit(1)

# 3. Load Instructor Public Key
try:
    with open("instructor_public.pem", "rb") as f:
        instructor_public_key = serialization.load_pem_public_key(f.read())
except FileNotFoundError:
    print("Error: 'instructor_public.pem' not found.")
    sys.exit(1)

# 4. Sign the hash
signature = student_private_key.sign(
    commit_hash.encode(),
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

# 5. Encrypt the signature
encrypted_signature = instructor_public_key.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# 6. Print the result
print("\n=== COPY THIS SIGNATURE ===")
print(base64.b64encode(encrypted_signature).decode('utf-8'))
print("===========================\n")