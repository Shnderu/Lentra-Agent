#!/bin/bash

set -e

echo "[1] Restarting API..."
systemctl daemon-reload
systemctl restart lentra-api.service

echo "[2] Waiting startup..."
sleep 2

echo "[3] Health check..."
curl -s http://localhost:8000/health || echo "HEALTH FAILED"

echo "[4] Smoke test..."
/opt/lentra/infra/scripts/smoke_test.sh

echo "[DONE]"
