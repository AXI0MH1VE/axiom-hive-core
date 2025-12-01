import os, json, zipfile, time, hashlib
from ssot.registry import load_version, load_rules

os.makedirs("artifacts", exist_ok=True)

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda: f.read(8192), b""): h.update(c)
    return h.hexdigest()

axioms = load_version("current")
rules = load_rules()
prov = "artifacts/provenance_chain.json"
dash = "artifacts/dashboard.json"

# Build manifest with hashes
manifest = {
    "docId": "AH-Ω-C0-2025-11-30",
    "generated_at": time.time(),
    "axioms_version": axioms["version"],
    "axioms_hash": hashlib.sha256(json.dumps(axioms, sort_keys=True).encode()).hexdigest(),
    "rules_hash": hashlib.sha256(json.dumps(rules, sort_keys=True).encode()).hexdigest(),
    "provenance_file": prov, "provenance_sha256": sha256(prov) if os.path.exists(prov) else None,
    "dashboard_file": dash, "dashboard_sha256": sha256(dash) if os.path.exists(dash) else None,
    "C": json.load(open(dash))["C"] if os.path.exists(dash) else None
}
json.dump(manifest, open("artifacts/manifest.json","w"), indent=2, sort_keys=True)

# Zip audit pack
with zipfile.ZipFile("artifacts/axiom-hive-audit-pack.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in ["artifacts/provenance_chain.json","artifacts/dashboard.json","artifacts/manifest.json","ssot/axioms/v1.0.1/axioms.json","ssot/rules/inference_rules.json"]:
        if os.path.exists(p): z.write(p)
print("Wrote artifacts/axiom-hive-audit-pack.zip")