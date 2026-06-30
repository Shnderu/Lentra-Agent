#!/bin/bash

TARGET="/opt/lentra/infra/lentra/core/market_intelligence/pipeline/intelligence_pipeline_orchestrator.py"

echo "[FIX] Redirecting trace import to safe location"

sed -i 's|from lentra.core.bootstrap.runtime_trace_audit|from lentra.core.market_intelligence.trace.runtime_trace_audit|g' "$TARGET"

echo "[OK] Import redirected"
