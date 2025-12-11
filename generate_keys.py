from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys():
    print("Generating RSA 4096-bit Key Pair...")
    
    # 1. Generate the private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    # 2. Save the Private Key (student_private.pem)
    with open("student_private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print("✅ student_private.pem created.")

    # 3. Generate the Public Key (student_public.pem)
    public_key = private_key.public_key()
    with open("student_public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print("✅ student_public.pem created.")

if __name__ == "__main__":
    generate_keys()