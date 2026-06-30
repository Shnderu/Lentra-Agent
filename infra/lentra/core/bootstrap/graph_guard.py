"""
BOOTSTRAP GRAPH GUARD v1
Prevents circular or illegal imports at runtime.
"""

import sys
import importlib
from typing import Set

ALLOWED_IMPORTS = {
    "lentra.core.bootstrap",
    "lentra.core.market_intelligence.build",
    "lentra.core.market_intelligence.gateway",
    "lentra.core.market_intelligence.pipeline.intelligence_pipeline_orchestrator",
}

BLOCKED_PATTERNS = [
    ("bootstrap", "gateway"),
    ("gateway", "bootstrap"),
    ("orchestrator", "build"),
    ("pipeline", "build"),
]

def validate_import_chain(module_name: str, importer: str):
    for a, b in BLOCKED_PATTERNS:
        if a in importer and b in module_name:
            raise ImportError(
                f"BOOTSTRAP CYCLE BLOCKED: {importer} → {module_name}"
            )

def safe_import(name: str):
    frame = sys._getframe(1)
    importer = frame.f_globals.get("__name__", "unknown")

    validate_import_chain(name, importer)

    return importlib.import_module(name)
