#!/bin/bash
set -e

echo "[1] Restart API"
systemctl restart lentra-api.service

sleep 2

echo "[2] Smoke test"
bash /opt/lentra/infra/scripts/smoke_test.sh

echo "[DONE]"
