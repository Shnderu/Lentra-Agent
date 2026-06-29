#!/bin/bash

set -e

echo "[1] Restart API"
systemctl daemon-reload
systemctl restart lentra-api.service

echo "[2] Wait"
sleep 2

echo "[3] Smoke"
/opt/lentra/infra/scripts/smoke_test.sh

echo "[DONE]"
