import hashlib, json, os
TARGETS = ["ssot/axioms/v1.0.1/axioms.json", "ssot/rules/inference_rules.json", "api_server.py"]
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(8192), b""): h.update(c)
    return h.hexdigest()
hashes = {t: sha256(t) for t in TARGETS if os.path.exists(t)}
json.dump(hashes, open("build_hashes.json", "w"), indent=2, sort_keys=True)
print("Integrity hashes written:", len(hashes))