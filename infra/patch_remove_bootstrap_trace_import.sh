#!/bin/bash

TARGET="/opt/lentra/infra/lentra/core/market_intelligence/pipeline/intelligence_pipeline_orchestrator.py"

echo "[FIX] Removing invalid bootstrap.trace import"

sed -i 's|from lentra.core.bootstrap.runtime_trace_audit import RuntimeTraceAudit||g' "$TARGET"

echo "[OK] Import removed safely"
