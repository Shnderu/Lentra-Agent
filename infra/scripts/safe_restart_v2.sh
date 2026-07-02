#!/usr/bin/env bash

set +e

LOG="/tmp/lentra_final_lock.log"
exec > >(tee -a "$LOG") 2>&1

echo "=============================="
echo "LENTRA GRAPH CONTRACT v2 LOCK"
echo "=============================="

systemctl restart lentra-api

echo ""
echo "[WAIT STABILIZATION]"
for i in {1..10}; do
  echo "check $i"
  curl -s --max-time 2 localhost:8000/health && break
  sleep 2
done

echo ""
echo "[BASE TEST]"
curl -s -X POST localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query":"studio da nang 700",
    "price":700,
    "market_price":630
  }' || echo "BASE FAIL"

echo ""
echo "[GRAPH V2 TEST]"
curl -s -X POST localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query":"studio da nang 700",
    "price":700,
    "market_price":630,
    "graph_v2": true
  }' || echo "GRAPH FAIL"

echo ""
echo "LOCK COMPLETE"
echo "LOG: $LOG"
