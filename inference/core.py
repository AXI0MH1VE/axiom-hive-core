from dataclasses import dataclass
from typing import List, Dict, Optional
import time, json, hashlib

@dataclass
class ProofTrace:
    steps: List[Dict]
    axioms_used: List[str]
    rules_applied: List[str]
    conclusion: str

@dataclass
class InferenceResult:
    output: str
    proof: ProofTrace
    metadata: Dict

class InferenceCore:
    def __init__(self, axiom_set: Dict, rule_set: Dict, kb: Dict):
        self.axiom_set = axiom_set
        self.rule_set = rule_set
        self.kb = kb

    def _statement_hash(self, statement: str, source: str) -> str:
        b = json.dumps({"statement": statement, "source": source}, sort_keys=True).encode()
        return hashlib.sha256(b).hexdigest()

    def infer(self, query: str) -> Optional[InferenceResult]:
        # Minimal demo: treat query as fact_id and derive its statement/source
        fact = next((f for f in self.kb.get("facts", []) if f["id"] == query), None)
        if not fact:
            return None
        conclusion = f'STMT("{fact["statement"]}")'
        steps = [{"rule": "universal_instantiation", "premises": [f'AX({self.axiom_set["version"]})'], "conclusion": conclusion}]
        proof = ProofTrace(steps=steps, axioms_used=["AX001"], rules_applied=["universal_instantiation"], conclusion=conclusion)
        meta = {"solver": "axiom-demo", "version": self.axiom_set["version"], "timestamp": time.time()}
        return InferenceResult(output=conclusion, proof=proof, metadata=meta)