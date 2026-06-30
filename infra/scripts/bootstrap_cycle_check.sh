#!/usr/bin/env bash

echo "=============================="
echo "BOOTSTRAP CYCLE CHECK"
echo "=============================="

echo "[1] checking build import safety..."
grep -n "gateway import" /opt/lentra/infra/lentra/core/market_intelligence/build.py || echo "OK: lazy import only"

echo ""
echo "[2] checking gateway ownership rule..."
grep -n "Orchestrator(" /opt/lentra/infra/lentra/core/market_intelligence/gateway.py || echo "OK: no internal creation"

echo ""
echo "[3] bootstrap entry clean..."
grep -n "build_intelligence_gateway" /opt/lentra/infra/lentra/core/bootstrap.py

echo ""
echo "=============================="
echo "DONE"
echo "=============================="
