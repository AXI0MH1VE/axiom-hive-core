import json, hashlib
from dataclasses import dataclass
from typing import Dict
from inference.core import ProofTrace

@dataclass
class VerificationResult:
    valid: bool
    reason: str
    checked_steps: int

class ProofVerifier:
    def __init__(self, axiom_set: Dict, rule_set: Dict):
        self.axioms = axiom_set
        self.rules = rule_set

    def _axiom_hash(self, axiom_set: Dict) -> str:
        return hashlib.sha256(json.dumps(axiom_set, sort_keys=True).encode()).hexdigest()

    def verify(self, output: str, proof: ProofTrace, expected_axiom_hash: str) -> VerificationResult:
        actual = self._axiom_hash(self.axioms)
        if actual != expected_axiom_hash:
            return VerificationResult(False, "axiom_hash_mismatch", 0)
        # Very simple check: ensure steps list exists and final conclusion matches
        for i, step in enumerate(proof.steps):
            if step.get("rule") not in [r["name"] for r in self.rules["rules"]]:
                return VerificationResult(False, f"unknown_rule:{step.get('rule')}", i)
            if "conclusion" not in step:
                return VerificationResult(False, f"missing_conclusion_at_step:{i}", i)
        if proof.conclusion != output:
            return VerificationResult(False, "conclusion_mismatch", len(proof.steps))
        return VerificationResult(True, "ok", len(proof.steps))