# Axiom Hive Core API Documentation

## Base URL

```
http://localhost:8080
```

## Endpoints

### Health Check

**GET** `/health`

Returns operational status and timestamp.

**Response:**
```json
{
  "status": "operational",
  "timestamp": 1733034000.0
}
```

### Proof-Carrying Inference

**POST** `/infer`

Performs inference with cryptographic proof generation.

**Request Body:**
```json
{
  "input": "KB001",
  "axiom_version": "current"
}
```

**Parameters:**
- `input` (required): Fact ID from knowledge base
- `axiom_version` (optional): Axiom version to use (default: "current")

**Response (Success):**
```json
{
  "output": "STMT(\"Co-administration of Drug A and Drug B is contraindicated.\")",
  "proof": {
    "steps": [
      {
        "rule": "universal_instantiation",
        "premises": ["AX(1.0.1)"],
        "conclusion": "STMT(...)"
      }
    ],
    "axioms_used": ["AX001"],
    "rules_applied": ["universal_instantiation"],
    "conclusion": "STMT(...)"
  },
  "provenance": {
    "input_hash": "abc123...",
    "axiom_hash": "def456...",
    "rule_hash": "ghi789...",
    "output": "STMT(...)",
    "proof_hash": "jkl012...",
    "timestamp": 1733034000.0,
    "signature_b64": "..."
  },
  "status": "proven",
  "metadata": {
    "solver": "axiom-demo",
    "version": "1.0.1",
    "timestamp": 1733034000.0
  }
}
```

**Response (Undetermined):**
```json
{
  "output": "",
  "proof": {},
  "provenance": {},
  "status": "undetermined",
  "metadata": {
    "reason": "No valid derivation"
  }
}
```

**Error (Verification Failed):**
```json
{
  "detail": "verification_failed:axiom_hash_mismatch"
}
```

### Get Axioms

**GET** `/axioms/{version}`

Retrieves axiom set for specified version.

**Parameters:**
- `version`: Version identifier (e.g., "1.0.1", "current")

**Response:**
```json
{
  "version": "1.0.1",
  "timestamp": "2025-09-06T21:42:29Z",
  "authority": "system_operator",
  "axioms": [
    {
      "id": "AX001",
      "statement": "∀x: Entity(x) → HasIdentifier(x)",
      "domain": "core",
      "priority": 1
    }
  ],
  "hash": "sha256:..."
}
```

### Verify Provenance

**GET** `/verify/{idx}`

Verifies provenance record by index.

**Parameters:**
- `idx`: Record index (integer)

**Response:**
```json
{
  "valid": true,
  "record_index": 0
}
```

## Status Codes

- `200` - Success
- `500` - Verification failed (consistency error)

## Consistency Guarantee

**C=0**: All accepted outputs have valid proofs. Outputs without valid proofs are rejected with HTTP 500.

## Example Usage

```bash
# Health check
curl http://localhost:8080/health

# Inference with proof
curl -X POST http://localhost:8080/infer \
  -H 'Content-Type: application/json' \
  -d '{"input":"KB001","axiom_version":"current"}'

# Get current axioms
curl http://localhost:8080/axioms/current

# Verify provenance
curl http://localhost:8080/verify/0
```