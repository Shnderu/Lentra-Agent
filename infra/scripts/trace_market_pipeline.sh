#!/bin/bash

set -e

echo "===== MarketIntelligenceEngine ====="
grep -n "VerdictEngine\|RiskEngine\|RankingEngine\|ConfidenceEngine\|Area" \
/opt/lentra/infra/lentra/core/market_intelligence/market_intelligence_engine.py

echo
echo "===== VerdictEngine ====="
grep -n "class VerdictEngine\|compute_unified_score\|def run" \
/opt/lentra/infra/lentra/core/market_intelligence/verdict/verdict_engine.py

echo
echo "===== RiskEngine ====="
grep -n "class RiskEngine\|def evaluate" \
/opt/lentra/infra/lentra/core/market_intelligence/risk/risk_engine.py

echo
echo "===== ConfidenceEngine ====="
grep -n "class ConfidenceEngine\|def run" \
/opt/lentra/infra/lentra/core/market_intelligence/confidence/confidence_engine.py

echo
echo "===== RankingEngine ====="
grep -n "class RankingEngine\|def score" \
/opt/lentra/infra/lentra/core/market_intelligence/decision/ranking_engine.py
