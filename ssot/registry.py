import os, json, hashlib
from typing import Dict

BASE = os.path.join("ssot", "axioms")

def load_version(version: str) -> Dict:
    if version == "current":
        version = os.readlink(os.path.join(BASE, "current"))
    path = os.path.join(BASE, version, "axioms.json")
    axioms = json.load(open(path, "r"))
    axioms["hash"] = hashlib.sha256(json.dumps(axioms, sort_keys=True).encode()).hexdigest()
    return axioms

def load_rules() -> Dict:
    return json.load(open(os.path.join("ssot", "rules", "inference_rules.json"), "r"))