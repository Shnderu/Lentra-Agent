"""
Compatibility shim.

Real implementation lives in:
lentra.core.market_intelligence.gateway.graph_adapter

This file exists ONLY to fix import drift without refactoring core graph system.
"""

from lentra.core.market_intelligence.gateway.graph_adapter import GraphAdapter

__all__ = ["GraphAdapter"]
