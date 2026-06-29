#!/bin/bash

set -e

echo "[CHECK] Legacy references..."

grep -R "MarketIntelligenceEngineV2" /opt/lentra/infra/lentra || echo "OK"
grep -R "services.market_intelligence" /opt/lentra/infra/lentra || echo "OK"
grep -R "core.v2" /opt/lentra/infra/lentra || echo "OK"

echo "[CHECK] Core exists:"
test -f /opt/lentra/infra/lentra/core/market_intelligence/market_intelligence_engine.py && echo "OK"
