#!/usr/bin/env bash

set -e

echo "=============================="
echo " INTELLIGENCE GRAPH HEALTH"
echo "=============================="

echo ""
echo "[1] PYTHON IMPORT CHECK"
python3 - << 'PY'
import sys

modules = [
    "lentra.core.bootstrap",
    "lentra.core.market_intelligence.build",
    "lentra.core.market_intelligence.gateway",
    "lentra.core.market_intelligence.engine",
]

print("\n-- import status --")
for m in modules:
    try:
        __import__(m)
        print(f"[OK] {m}")
    except Exception as e:
        print(f"[FAIL] {m} -> {e}")
PY

echo ""
echo "[2] ORCHESTRATOR GRAPH CHECK"
python3 - << 'PY'
try:
    from lentra.core.intelligence.orchestrator import Orchestrator
    print("[OK] core orchestrator import")
except Exception as e:
    print("[FAIL] orchestrator import:", e)

try:
    from lentra.core.execution.build_intelligence_stack import build_intelligence_gateway
    print("[OK] execution stack builder import")
except Exception as e:
    print("[FAIL] execution stack:", e)
PY

echo ""
echo "[3] MARKET INTELLIGENCE CORE CHECK"
python3 - << 'PY'
critical_layers = [
    "lentra.core.market_intelligence.dedup.dedup_engine_v2",
    "lentra.core.market_intelligence.ranking.unified_ranking_engine",
    "lentra.core.market_intelligence.risk.risk_engine_v2",
    "lentra.core.market_intelligence.pricing.price_engine",
    "lentra.core.market_intelligence.area.area_engine_v2",
    "lentra.core.market_intelligence.explanation.unified_explainer",
]

print("\n-- core intelligence layers --")
for m in critical_layers:
    try:
        __import__(m)
        print(f"[OK] {m}")
    except Exception as e:
        print(f"[WARN] {m} -> {e}")
PY

echo ""
echo "[4] GATEWAY INITIALIZATION TEST"
python3 - << 'PY'
try:
    from lentra.core.market_intelligence.build import build_intelligence_gateway
    gw = build_intelligence_gateway(orchestrator={"execute": lambda x: x})
    print("[OK] gateway build successful")
except Exception as e:
    print("[FAIL] gateway build:", e)
PY

echo ""
echo "[5] PIPELINE GRAPH VALIDATION"
python3 - << 'PY'
try:
    from lentra.core.pipeline.context import PipelineContext
    from lentra.core.pipeline.pipeline import Pipeline
    print("[OK] pipeline core available")
except Exception as e:
    print("[FAIL] pipeline core:", e)
PY

echo ""
echo "=============================="
echo " HEALTH CHECK COMPLETE"
echo "=============================="
