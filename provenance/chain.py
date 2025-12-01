import hashlib, time, base64, json, os
from dataclasses import dataclass, asdict
from typing import List, Dict
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import Base64Encoder

@dataclass
class ProvenanceRecord:
    input_hash: str
    axiom_hash: str
    rule_hash: str
    output: str
    proof_hash: str
    timestamp: float
    signature_b64: str

    def to_dict(self): return asdict(self)

class ProvenanceChain:
    def __init__(self):
        self.records: List[ProvenanceRecord] = []
        self._keys_path = "keys/ed25519.json"
        self._sk, self._vk = self._load_or_create_keys()

    def _load_or_create_keys(self):
        try:
            kp = json.load(open(self._keys_path, "r"))
            sk = SigningKey(Base64Encoder.decode(kp["sk"]), encoder=Base64Encoder)
            vk = VerifyKey(Base64Encoder.decode(kp["vk"]), encoder=Base64Encoder)
            return sk, vk
        except:
            sk = SigningKey.generate(); vk = sk.verify_key
            kp = {"sk": Base64Encoder.encode(sk.encode()).decode(), "vk": Base64Encoder.encode(vk.encode()).decode()}
            os.makedirs("keys", exist_ok=True)
            json.dump(kp, open(self._keys_path, "w"), indent=2, sort_keys=True)
            return sk, vk

    def create_record(self, input_data: str, axiom_set: Dict, rule_set: Dict, output: str, proof: Dict) -> ProvenanceRecord:
        input_hash = hashlib.sha256(input_data.encode()).hexdigest()
        axiom_hash = hashlib.sha256(json.dumps(axiom_set, sort_keys=True).encode()).hexdigest()
        rule_hash = hashlib.sha256(json.dumps(rule_set, sort_keys=True).encode()).hexdigest()
        proof_hash = hashlib.sha256(json.dumps(proof, sort_keys=True).encode()).hexdigest()
        combined = f"{input_hash}|{axiom_hash}|{rule_hash}|{output}|{proof_hash}".encode()
        sig = self._sk.sign(hashlib.sha256(combined).digest()).signature
        rec = ProvenanceRecord(
            input_hash=input_hash, axiom_hash=axiom_hash, rule_hash=rule_hash,
            output=output, proof_hash=proof_hash, timestamp=time.time(),
            signature_b64=base64.b64encode(sig).decode()
        )
        self.records.append(rec)
        return rec

    def verify_record(self, record: ProvenanceRecord) -> bool:
        combined = f"{record.input_hash}|{record.axiom_hash}|{record.rule_hash}|{record.output}|{record.proof_hash}".encode()
        try:
            self._vk.verify(hashlib.sha256(combined).digest(), base64.b64decode(record.signature_b64.encode()))
            return True
        except Exception:
            return False

    def export_chain(self, path: str):
        json.dump([r.to_dict() for r in self.records], open(path, "w"), indent=2, sort_keys=True)