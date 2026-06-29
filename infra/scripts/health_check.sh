#!/bin/bash

set -e

echo "[HEALTH] API check..."

curl -s http://localhost:8000/health || echo "HEALTH FAILED"

echo "[PROCESS]"
ps aux | grep lentra | grep -v grep || echo "NO PROCESS"

echo "[LOGS]"
journalctl -u lentra-api.service -n 50 --no-pager
