from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import json, hashlib, os, sys

def sign_axioms(axioms_path: str, private_key_path: str, output_path: str) -> str:
    axioms = json.load(open(axioms_path, "r"))
    content = json.dumps(axioms, sort_keys=True).encode()
    digest = hashlib.sha256(content).digest()
    private_key = serialization.load_pem_private_key(open(private_key_path, "rb").read(), password=None)
    signature = private_key.sign(digest)
    open(output_path, "wb").write(signature)
    return hashlib.sha256(content).hexdigest()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python ssot/sign_axioms.py <axioms.json> <privkey.pem> <signature.sig>")
        sys.exit(1)
    h = sign_axioms(sys.argv[1], sys.argv[2], sys.argv[3])
    print("Axiom content hash:", h)