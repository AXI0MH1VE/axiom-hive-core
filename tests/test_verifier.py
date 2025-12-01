from verification.verifier import ProofVerifier
from inference.core import ProofTrace
import json, hashlib

def test_verifier_pass():
    ax = {"version": "1.0.1", "axioms": [{"id":"AX001","statement":"∀x: Entity(x) → HasIdentifier(x)"}]}
    ax["hash"] = hashlib.sha256(json.dumps(ax, sort_keys=True).encode()).hexdigest()
    rules = {"rules":[{"name":"universal_instantiation"}]}
    v = ProofVerifier(ax, rules)
    proof = ProofTrace(steps=[{"rule":"universal_instantiation","conclusion":"STMT(\"S\")"}], axioms_used=["AX001"], rules_applied=["universal_instantiation"], conclusion="STMT(\"S\")")
    res = v.verify("STMT(\"S\")", proof, ax["hash"])
    assert res.valid

def test_verifier_fail_hash_mismatch():
    ax = {"version":"1.0.1","axioms":[]}; ax["hash"] = "deadbeef"
    rules = {"rules":[{"name":"universal_instantiation"}]}
    v = ProofVerifier(ax, rules)
    proof = ProofTrace(steps=[], axioms_used=[], rules_applied=[], conclusion="")
    res = v.verify("", proof, "cafebabe")
    assert not res.valid and res.reason == "axiom_hash_mismatch"