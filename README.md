# AXIOM HIVE — Sovereign Intelligence — C=0

© 2025 Alexis Adams and Axiom Hive. All rights reserved.  
Document ID: AH-Ω-C0-2025-11-30  
**AXIOM HIVE™ • AXIOM INVARIANT CORE [Ω]™ • CONSISTENCY ERROR ZERO™**

[![CI/CD](https://github.com/AXI0MH1VE/axiom-hive-core/actions/workflows/deploy.yml/badge.svg)](https://github.com/AXI0MH1VE/axiom-hive-core/actions/workflows/deploy.yml)

## Production-Ready C=0 Architecture

### What is C=0?

**C=0** (Consistency Error Zero) means every accepted output carries a cryptographically signed proof verified against versioned axioms. If verification fails, the output is rejected—no exceptions.

### Architecture Components

- **SSOT Registry**: Versioned axioms and rules (content-addressed, signed)
- **Inference Core**: Generates candidate outputs with proof traces
- **Verification Gate**: Minimal proof checker; rejects unproven outputs
- **Cryptographic Provenance**: Signed, hash-linked records (Ed25519)
- **API Server**: FastAPI with proof-carrying responses
- **Kubernetes Ready**: Scalable production deployment (10 replicas default)
- **Continuous Auditing**: Real-time C=0 monitoring
- **CI/CD Pipeline**: Reproducibility checks, tests, Docker builds

## Quick Start

### Docker (Fastest)

```bash
docker build -t axiomhive/core . && docker run -p 8080:8080 axiomhive/core
```

Test it:
```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/infer \
  -H 'Content-Type: application/json' \
  -d '{"input":"KB001"}'
```

### Local Development

```bash
# Clone and setup
git clone https://github.com/AXI0MH1VE/axiom-hive-core.git
cd axiom-hive-core

# Virtual environment
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.lock

# Create axiom symlink
cd ssot/axioms && ln -sf v1.0.1 current && cd ../..

# Run tests
pytest -q

# Start server
uvicorn api_server:app --host 0.0.0.0 --port 8080
```

### Kubernetes Production Deployment

```bash
kubectl create namespace production
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deploy/axiom-hive -n production
```

## API Endpoints

### Health Check
```bash
GET /health
```

### Proof-Carrying Inference
```bash
POST /infer
{
  "input": "KB001",
  "axiom_version": "current"
}
```

**Response includes:**
- `output`: Derived statement
- `proof`: Step-by-step derivation with axioms/rules used
- `provenance`: Cryptographically signed record
- `status`: "proven" or "undetermined"

### Get Axioms
```bash
GET /axioms/{version}
```

### Verify Provenance
```bash
GET /verify/{idx}
```

## Provenance & Auditing

### Generate Demo Proofs and Audit Pack

```bash
# Start API
uvicorn api_server:app --host 0.0.0.0 --port 8080 &

# Run demo (generates proofs)
python scripts/run_demo_and_export.py

# Create audit pack
python scripts/generate_audit_pack.py

# View artifacts
ls -lh artifacts/
```

**Audit pack includes:**
- `provenance_chain.json` - All signed proof records
- `dashboard.json` - C=0 metrics summary
- `manifest.json` - File hashes and metadata
- `axiom-hive-audit-pack.zip` - Complete bundle

## Container Registry

### Pull from GHCR

```bash
docker pull ghcr.io/axi0mh1ve/axiom-hive-core:latest
docker run -p 8080:8080 ghcr.io/axi0mh1ve/axiom-hive-core:latest
```

### Build and Push

```bash
IMAGE="ghcr.io/axi0mh1ve/axiom-hive-core:1.0.0"
echo "${GHCR_TOKEN}" | docker login ghcr.io -u AXI0MH1VE --password-stdin
docker build -t ${IMAGE} .
docker push ${IMAGE}
```

## Release Process

```bash
# Tag release
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions automatically:
# - Builds and pushes to GHCR
# - Creates GitHub release
# - Attaches build hashes
```

## Axiom Updates

To update the axiom set with cryptographic verification:

```bash
# Create new version
mkdir -p ssot/axioms/v1.0.2
cp ssot/axioms/v1.0.1/*.{json,fol,yaml} ssot/axioms/v1.0.2/

# Edit axioms
vim ssot/axioms/v1.0.2/axioms.json

# Sign with private key
python ssot/sign_axioms.py \
  ssot/axioms/v1.0.2/axioms.json \
  keys/axioms_privkey.pem \
  ssot/axioms/v1.0.2/signature.sig

# Update current pointer
rm ssot/axioms/current && ln -s v1.0.2 ssot/axioms/current

# Commit
git add ssot/axioms/v1.0.2 ssot/axioms/current
git commit -m "SSOT: bump to v1.0.2 (signed)"
git push
```

## Documentation

- **[Operations Guide](OPERATIONS.md)** - Complete deployment and maintenance procedures
- **[API Documentation](docs/API.md)** - Full API reference with examples
- **[Architecture](docs/ARCHITECTURE.md)** - System design and C=0 proof

## Project Structure

```
axiom-hive-core/
├── README.md                  # This file
├── OPERATIONS.md              # Operations playbook
├── requirements.lock          # Pinned dependencies
├── Dockerfile                 # Container build
├── flake.nix                  # Reproducible Nix build
├── .github/workflows/         # CI/CD pipelines
├── ssot/                      # Single Source of Truth
│   ├── axioms/                # Versioned axiom sets
│   ├── rules/                 # Inference rules
│   ├── sign_axioms.py         # Cryptographic signing
│   └── registry.py            # Version loader
├── data/                      # Knowledge base
├── inference/                 # Inference engine
├── verification/              # Proof verifier
├── provenance/                # Cryptographic chain
├── api_server.py              # FastAPI application
├── k8s/                       # Kubernetes manifests
├── monitoring/                # Audit daemon
├── scripts/                   # Utility scripts
└── tests/                     # Test suite
```

## Testing

```bash
# Run all tests
pytest -v

# Run specific test
pytest tests/test_verifier.py -v

# Validate C=0 across 100 inferences
pytest tests/validate_c0.py -v
```

## Monitoring

```bash
# Run continuous audit
python monitoring/audit_daemon.py
```

The daemon samples provenance records every 5 minutes and verifies signatures. C value is logged (should always be 0).

## License

© 2025 Alexis Adams and Axiom Hive. All rights reserved.

## Contact

- **Website**: [axiomhive.com](https://axiomhive.com)
- **GitHub**: [@AXI0MH1VE](https://github.com/AXI0MH1VE)
- **X/Twitter**: [@devdollzai](https://x.com/devdollzai)

---

**AXIOM HIVE™ • C=0™ • Built with Mathematical Certainty**