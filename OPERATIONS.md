# Axiom Hive Core - Operations Playbook

## Quick Start

### Local Development

```bash
# Clone and setup
git clone https://github.com/AXI0MH1VE/axiom-hive-core.git
cd axiom-hive-core

# Virtual environment
python -m venv .venv && source .venv/bin/activate
pip install --no-deps -r requirements.lock

# Create symlink for current axioms
cd ssot/axioms && ln -sf v1.0.1 current && cd ../..

# Run tests
pytest -q

# Start API server
uvicorn api_server:app --host 0.0.0.0 --port 8080 &
sleep 2

# Health check
curl -s http://localhost:8080/health | jq

# Proof-carrying inference
curl -s -X POST http://localhost:8080/infer \
  -H 'Content-Type: application/json' \
  -d '{"input":"KB001","axiom_version":"current"}' | jq
```

### Docker Operations

```bash
# Build
docker build -t axiomhive/core:dev .

# Run
docker run -p 8080:8080 --name axiom-hive-core axiomhive/core:dev

# Test
curl -s http://localhost:8080/health | jq
curl -s -X POST http://localhost:8080/infer \
  -H 'Content-Type: application/json' \
  -d '{"input":"KB001"}' | jq
```

### GHCR Publishing

```bash
# Login to GitHub Container Registry
echo "${GHCR_TOKEN}" | docker login ghcr.io -u AXI0MH1VE --password-stdin

# Build and push
IMAGE="ghcr.io/axi0mh1ve/axiom-hive-core:1.0.0"
docker build -t ${IMAGE} .
docker push ${IMAGE}
```

## Provenance & Auditing

### Generate Signing Keys

```bash
python scripts/gen_public_key.py
```

### Run Demo and Export Provenance

```bash
# Start API if not running
uvicorn api_server:app --host 0.0.0.0 --port 8080 &
sleep 2

# Run demo (generates proofs)
python scripts/run_demo_and_export.py

# Generate audit pack
python scripts/generate_audit_pack.py

# Check artifacts
ls -lh artifacts/
```

### Audit Pack Contents

- `provenance_chain.json` - Signed, hash-linked proof records
- `dashboard.json` - C=0 summary with metrics
- `manifest.json` - Axioms/rules hashes and file integrity
- `axiom-hive-audit-pack.zip` - Complete bundle for auditors

## Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace production || true

# Deploy
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl rollout status deploy/axiom-hive -n production
kubectl get svc axiom-hive-service -n production

# Get external IP
kubectl get svc axiom-hive-service -n production -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

## Axiom Updates (Version Bump)

```bash
# Create new version
mkdir -p ssot/axioms/v1.0.2
cp ssot/axioms/v1.0.1/*.{json,fol,yaml} ssot/axioms/v1.0.2/

# Edit axioms as needed
vim ssot/axioms/v1.0.2/axioms.json

# Sign new version (requires private key)
python ssot/sign_axioms.py \
  ssot/axioms/v1.0.2/axioms.json \
  keys/axioms_privkey.pem \
  ssot/axioms/v1.0.2/signature.sig

# Update current symlink
rm ssot/axioms/current
ln -s v1.0.2 ssot/axioms/current

# Commit and deploy
git add ssot/axioms/v1.0.2 ssot/axioms/current
git commit -m "SSOT: bump to v1.0.2 (signed)"
git push
```

## Release Process

```bash
# Create release branch
git checkout -b release/v1.0.0
git commit --allow-empty -m "release: v1.0.0"

# Tag release
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will automatically:
# - Build and push to GHCR
# - Create GitHub release
# - Attach build artifacts
```

## Public Proof Dump

```bash
# Generate public artifacts
mkdir -p public
cp artifacts/dashboard.json public/
cp artifacts/provenance_chain.json public/
jq '{version, axioms: [.axioms[].id], hash}' \
  ssot/axioms/v1.0.1/axioms.json > public/axioms_meta.json

# Serve via GitHub Pages (enable in repo settings)
```

## End-to-End Smoke Test

```bash
set -e

# Setup
python -m venv .venv && source .venv/bin/activate
pip install --no-deps -r requirements.lock
cd ssot/axioms && ln -sf v1.0.1 current && cd ../..

# Test
pytest -q

# Run API
uvicorn api_server:app --host 0.0.0.0 --port 8080 &
sleep 2

# Generate proofs
for i in {1..3}; do
  curl -s -X POST http://localhost:8080/infer \
    -H 'Content-Type: application/json' \
    -d '{"input":"KB001"}' >/dev/null
done

# Export and package
python scripts/run_demo_and_export.py
python scripts/generate_audit_pack.py

# Build and publish
docker build -t ghcr.io/axi0mh1ve/axiom-hive-core:demo .
echo "${GHCR_TOKEN}" | docker login ghcr.io -u AXI0MH1VE --password-stdin
docker push ghcr.io/axi0mh1ve/axiom-hive-core:demo

echo "✅ Complete: Local proof, audit pack, and image publish"
```

## Auditor Handoff

Provide external auditors with:

1. **Audit Pack**: `artifacts/axiom-hive-audit-pack.zip`
2. **Build Hashes**: `build_hashes.json`
3. **Container Image**: `ghcr.io/axi0mh1ve/axiom-hive-core:1.0.0`
4. **API Access**: Health/infer endpoints or K8s credentials
5. **Documentation**: This operations guide

## Monitoring

```bash
# Run continuous audit daemon
python monitoring/audit_daemon.py

# Check C value (should always be 0)
tail -f audit.log | grep "Audit C="
```

## Troubleshooting

### Symlink Missing
```bash
cd ssot/axioms && ln -sf v1.0.1 current && cd ../..
```

### Import Errors
```bash
export PYTHONPATH=$PWD:$PYTHONPATH
```

### Port Already in Use
```bash
lsof -ti:8080 | xargs kill -9
```

### Docker Build Fails
```bash
docker system prune -af
docker build --no-cache -t axiomhive/core .
```