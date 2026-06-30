#!/usr/bin/env bash

set -euo pipefail

BASE="/opt/lentra/infra/lentra"

echo "=============================="
echo " INTELLIGENCE GRAPH HEALTH CHECK"
echo "=============================="

echo ""
echo "[1] CORE MARKET INTELLIGENCE ENTRY POINTS"
echo "------------------------------------------"
find "$BASE/core/market_intelligence" -type f -name "*.py" | grep -E "build|gateway|engine|orchestrator|pipeline" || true

echo ""
echo "[2] EXECUTION / ORCHESTRATION LAYER"
echo "-----------------------------------"
find "$BASE/core/execution" -type f -name "*.py" || true

echo ""
echo "[3] BOOTSTRAP ENTRY POINTS"
echo "---------------------------"
find "$BASE/core" -maxdepth 3 -type f -name "bootstrap.py" || true
find "$BASE/core" -maxdepth 3 -type f -name "orchestrator.py" || true

echo ""
echo "[4] API ENTRY POINTS"
echo "---------------------"
find "$BASE/api" -type f -name "*.py" || true

echo ""
echo "[5] CRITICAL IMPORT GRAPH SNIFFER (build/gateway)"
echo "-------------------------------------------------"
grep -R "from lentra.core.market_intelligence.build" -n "$BASE" || true
grep -R "from lentra.core.market_intelligence.gateway" -n "$BASE" || true

echo ""
echo "[6] ORPHAN / CIRCULAR CANDIDATES"
echo "---------------------------------"
grep -R "build_intelligence_gateway" -n "$BASE" || true
grep -R "Orchestrator(" -n "$BASE" || true

echo ""
echo "[7] CORE INTELLIGENCE LAYERS SNAPSHOT"
echo "--------------------------------------"
ls -la "$BASE/core/market_intelligence" || true

echo ""
echo "[8] RANKING / DEDUP / RISK PRESENCE CHECK"
echo "------------------------------------------"
find "$BASE/core/market_intelligence" -type f | grep -E "dedup|risk|rank|scoring|pricing|geo" || true

echo ""
echo "[9] SUMMARY"
echo "-----------"
echo "Health check complete. Review output for:"
echo "- circular imports (build ↔ gateway)"
echo "- duplicate orchestrators"
echo "- split pipeline definitions"
echo "- overlapping ranking engines"

echo ""
echo "=============================="
echo " END HEALTH CHECK"
echo "=============================="
