import json, hashlib
from ssot.registry import load_version, load_rules
from inference.core import InferenceCore
from verification.verifier import ProofVerifier

KB = json.load(open("data/kb.json","r"))

def test_c0_across_100():
    ax = load_version("current"); rules = load_rules()
    core = InferenceCore(ax, rules, KB)
    verifier = ProofVerifier(ax, rules)
    accepted_failures = 0
    for i in range(100):
        # Alternate between known/unknown facts to test undetermined handling
        fid = "KB001" if i % 2 == 0 else "KBXXX"
        res = core.infer(fid)
        if res is None: continue
        v = verifier.verify(res.output, res.proof, ax["hash"])
        if not v.valid: accepted_failures += 1
    assert accepted_failures == 0  # C=0 among accepted verifications