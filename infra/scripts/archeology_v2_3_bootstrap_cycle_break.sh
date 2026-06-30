#!/usr/bin/env bash

set -e

echo "=============================="
echo " BOOTSTRAP CYCLE BREAK v2.3"
echo "=============================="

BOOT="/opt/lentra/infra/lentra/core/bootstrap.py"

echo "[1] Applying lazy gateway resolution"

cat << 'PYEOF' > $BOOT
"""
BOOTSTRAP STABILIZED (Archeology v2.3)
Cycle break: build ↔ gateway ↔ orchestrator
"""

def build_intelligence_gateway(orchestrator=None):
    # lazy import ONLY at runtime
    from lentra.core.market_intelligence.build import build_intelligence_gateway as _build

    return _build(orchestrator=orchestrator)


def bootstrap_intelligence_system():
    """
    SAFE ENTRYPOINT
    avoids circular import at module load time
    """
    from lentra.core.market_intelligence.pipeline.intelligence_pipeline_orchestrator import (
        IntelligencePipelineOrchestrator
    )

    pipeline = IntelligencePipelineOrchestrator()
    return pipeline
PYEOF

echo "[2] Hardening orchestrator lazy init"

ORCH="/opt/lentra/infra/lentra/core/intelligence/orchestrator.py"

cat << 'PYEOF' > $ORCH
class IntelligenceOrchestrator:

    def __init__(self, pipeline=None):
        self._pipeline = pipeline
        self._lazy_pipeline = None

    @property
    def pipeline(self):
        if self._lazy_pipeline is None:
            from lentra.core.market_intelligence.pipeline.intelligence_pipeline_orchestrator import (
                IntelligencePipelineOrchestrator
            )
            self._lazy_pipeline = IntelligencePipelineOrchestrator()
        return self._lazy_pipeline
PYEOF

echo "[3] Safe guard against double init in API layer"

API_PIPE="/opt/lentra/infra/lentra/api/pipeline.py"

cat << 'PYEOF' > $API_PIPE
from lentra.core.intelligence.orchestrator import IntelligenceOrchestrator

# SINGLETON SAFE INIT (no recursion)
pipeline = IntelligenceOrchestrator()
PYEOF

echo "[OK] BOOTSTRAP CYCLE BREAK APPLIED"
