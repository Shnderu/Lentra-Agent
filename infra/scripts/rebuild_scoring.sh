#!/bin/bash
set -e

echo "[1] Restart API"
systemctl restart lentra-api.service

echo "[2] Smoke test"
bash /opt/lentra/infra/scripts/smoke_test.sh

echo "[DONE]"
