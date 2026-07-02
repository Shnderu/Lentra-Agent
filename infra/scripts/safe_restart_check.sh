#!/usr/bin/env bash

set -euo pipefail

LOG_FILE="/tmp/lentra_safe_restart.log"

exec > >(tee -a "$LOG_FILE") 2>&1

echo "=============================="
echo "LENTRA SAFE RESTART CHECK"
echo "=============================="

echo ""
echo "[1] RESTART SERVICE (SAFE)"
systemctl restart lentra-api

echo ""
echo "[2] WAIT STABILIZATION"
sleep 5

echo ""
echo "[3] HEALTH CHECK"
curl --max-time 3 -s localhost:8000/health || echo "HEALTH FAILED"

echo ""
echo "[4] BASE SEARCH TEST"
curl --max-time 5 -s -X POST localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query":"studio da nang 700",
    "price":700,
    "market_price":630
  }' || echo "BASE FAILED"

echo ""
echo "[5] GRAPH V2 TEST"
curl --max-time 5 -s -X POST localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query":"studio da nang 700",
    "price":700,
    "market_price":630,
    "graph_v2": true
  }' || echo "GRAPH V2 FAILED"

echo ""
echo "=============================="
echo "DONE. LOG: $LOG_FILE"
echo "=============================="
