"""
CORE LOCKED MODULE

This module is disabled in CORE LOCK v2 architecture.

All orchestration responsibilities moved to:
- lentra.api.server (API layer)
- lentra.worker.engine (queue execution layer)
"""
def disabled():
    raise RuntimeError("Orchestrator is disabled in CORE LOCK v2")
