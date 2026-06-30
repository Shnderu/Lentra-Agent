#!/usr/bin/env bash

set -e

echo "=============================="
echo " GRAPH STABILIZATION PATCH v2.3"
echo "=============================="

ROOT="/opt/lentra/infra/lentra/core/market_intelligence"

echo "[1] Fixing graph engine import safety layer"

cat << 'PYEOF' > $ROOT/_import_safety.py
"""
GRAPH IMPORT SAFETY LAYER (Archeology v2.3)
Prevents circular dependency explosion between:
- build.py
- gateway.py
- orchestrator
"""

import importlib
import sys

_GRAPH_CACHE = {}

def safe_import(module_path: str):
    if module_path in _GRAPH_CACHE:
        return _GRAPH_CACHE[module_path]

    module = importlib.import_module(module_path)
    _GRAPH_CACHE[module_path] = module
    return module


def get_graph_engine():
    # lazy resolve to break circular dependency
    from lentra.core.market_intelligence.graph.market_graph_engine import MarketGraphEngine
    return MarketGraphEngine
PYEOF

echo "[2] Isolating graph engine entry (lazy load wrapper)"

cat << 'PYEOF' > $ROOT/graph/__init__.py
"""
Graph package stabilized entrypoint
Avoid direct engine import on module load
"""

def get_market_graph_engine():
    from .market_graph_engine import MarketGraphEngine
    return MarketGraphEngine
PYEOF

echo "[3] Protecting build.py from eager gateway import"

cat << 'PYEOF' > $ROOT/build.py
from typing import Optional

def build_intelligence_gateway(orchestrator: Optional[dict] = None):
    """
    STABILIZED BUILD (no eager imports)
    """
    from lentra.core.market_intelligence.gateway import IntelligenceGateway

    gateway = IntelligenceGateway(orchestrator=orchestrator or {})
    return gateway
PYEOF

echo "[OK] GRAPH STABILIZATION PATCH APPLIED"
