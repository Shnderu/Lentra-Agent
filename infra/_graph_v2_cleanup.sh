#!/bin/bash

set -e

BASE="/opt/lentra/infra/lentra"

echo "[GRAPH V2 CLEAN] Removing legacy layers..."

# API PATCHES
rm -f $BASE/api/search_patch.py || true
rm -f $BASE/api/search_graph_hook.py || true
rm -f $BASE/api/search_graph_v2_hook.py || true

# ENGINE LAYER (must not exist anymore)
rm -f $BASE/core/market_intelligence/engines/graph_v2_wrapper.py || true
rm -f $BASE/core/market_intelligence/engines/graph_v2_engine.py || true

# ENRICHMENT HOOKS
rm -f $BASE/core/market_intelligence/graph_v2/enrichment_hook.py || true
rm -f $BASE/core/market_intelligence/graph_v2/contract_enricher.py || true

# OLD TOGGLES / POLICIES (hard freeze decision)
rm -f $BASE/core/market_intelligence/graph_v2/feature_flag.py || true
rm -f $BASE/core/market_intelligence/graph_v2/feature_toggle.py || true
rm -f $BASE/core/market_intelligence/policy/graph_v2_policy.py || true

echo "[GRAPH V2 CLEAN] Done."
