#!/usr/bin/env bash

set +e

systemctl restart lentra-api

sleep 3

echo "=== HEALTH ==="
curl -s localhost:8000/health || echo "NO HEALTH"

echo ""
echo "=== BASE ==="
curl -s -X POST localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query":"studio da nang 700",
    "price":700,
    "market_price":630
  }' || echo "FAILED"

echo ""
echo "=== GRAPH V2 ==="
curl -s -X POST localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query":"studio da nang 700",
    "price":700,
    "market_price":630,
    "graph_v2": true
  }' || echo "FAILED"
