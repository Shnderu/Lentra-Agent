"""
Compatibility layer for legacy import:

lentra.core.market_intelligence.orchestrator.builder

Routes to unified intelligence orchestrator implementation.
"""

from typing import Any

# preferred modern implementation
from lentra.core.intelligence.orchestrator import Orchestrator


def build_orchestrator(*args, **kwargs) -> Any:
    """
    Legacy-compatible orchestrator factory.

    This exists ONLY to satisfy bootstrap dependency.
    """
    return Orchestrator(*args, **kwargs)
