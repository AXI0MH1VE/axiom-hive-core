import json, hashlib, os
axioms = json.load(open("ssot/axioms/v1.0.1/axioms.json", "r"))
digest = hashlib.sha256(json.dumps(axioms, sort_keys=True).encode()).hexdigest()
sig_path = "ssot/axioms/v1.0.1/signature.sig"
if not os.path.exists(sig_path):
    print("Signature missing (dev mode)."); exit(0)
sig = open(sig_path, "rb").read()
print("Axiom set hash:", digest, "| Signature bytes:", len(sig))