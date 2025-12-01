from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder
import json, os
os.makedirs("keys", exist_ok=True)
sk = SigningKey.generate()
vk = sk.verify_key
json.dump({"sk": Base64Encoder.encode(sk.encode()).decode(), "vk": Base64Encoder.encode(vk.encode()).decode()}, open("keys/ed25519.json", "w"), indent=2, sort_keys=True)
print("Keys written to keys/ed25519.json")