import json, time, requests, os
from provenance.chain import ProvenanceChain

API = "http://localhost:8080"
os.makedirs("artifacts", exist_ok=True)

# Smoke a batch across current axioms
for fid in ["KB001","KB002","KB001","KB002"]:
    r = requests.post(f"{API}/infer", json={"input": fid, "axiom_version":"current"}, timeout=10)
    r.raise_for_status()

# Export provenance chain snapshot
chain = ProvenanceChain()
chain.export_chain("artifacts/provenance_chain.json")

# Write a tiny dashboard summary
records = json.load(open("artifacts/provenance_chain.json","r"))
summary = {
    "count": len(records),
    "axiom_hashes": sorted({r["axiom_hash"] for r in records}),
    "last_ts": max(r["timestamp"] for r in records) if records else None,
    "C": 0  # accepted set is verified by gate
}
json.dump(summary, open("artifacts/dashboard.json","w"), indent=2, sort_keys=True)
print(json.dumps(summary, indent=2))