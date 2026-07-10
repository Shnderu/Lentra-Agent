"""
Compatibility wrapper.

Canonical runtime implementation:
    lentra.core.market_intelligence.isolation.engine_registry_v3

This module exists only to prevent legacy imports from creating
a second Market Intelligence registry implementation.
"""

from lentra.core.market_intelligence.isolation.engine_registry_v3 import (
    EngineRegistryV3,
    build_registry_v3,
)

__all__ = [
    "EngineRegistryV3",
    "build_registry_v3",
]
