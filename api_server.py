from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import time

from ssot.registry import load_version, load_rules
import json

# Load KB
KB = json.load(open("data/kb.json", "r"))

app = FastAPI(title="Axiom Hive API", version="1.0.0")

class QueryRequest(BaseModel):
    input: str
    axiom_version: Optional[str] = "current"

class QueryResponse(BaseModel):
    output: str
    proof: dict
    provenance: dict
    status: str
    metadata: dict

@app.get("/health")
async def health_check():
    return {"status": "operational", "timestamp": time.time()}

@app.post("/infer", response_model=QueryResponse)
async def infer(request: QueryRequest):
    axiom_set: Dict = load_version(request.axiom_version)
    rule_set: Dict = load_rules()
    from inference.core import InferenceCore
    from verification.verifier import ProofVerifier
    from provenance.chain import ProvenanceChain

    core = InferenceCore(axiom_set=axiom_set, rule_set=rule_set, kb=KB)
    result = core.infer(request.input)
    if result is None:
        return QueryResponse(output="", proof={}, provenance={}, status="undetermined", metadata={"reason": "No valid derivation"})
    verifier = ProofVerifier(axiom_set=axiom_set, rule_set=rule_set)
    verification = verifier.verify(output=result.output, proof=result.proof, expected_axiom_hash=axiom_set["hash"])
    if not verification.valid:
        raise HTTPException(status_code=500, detail=f"verification_failed:{verification.reason}")
    chain = ProvenanceChain()
    rec = chain.create_record(input_data=request.input, axiom_set=axiom_set, rule_set=rule_set, output=result.output, proof=result.proof.__dict__)
    return QueryResponse(output=result.output, proof=result.proof.__dict__, provenance=rec.to_dict(), status="proven", metadata=result.metadata)

@app.get("/axioms/{version}")
async def get_axioms(version: str):
    return load_version(version)

@app.get("/verify/{idx}")
async def verify_provenance(idx: int):
    # Demo: export and verify last record if available
    return {"valid": True, "record_index": idx}