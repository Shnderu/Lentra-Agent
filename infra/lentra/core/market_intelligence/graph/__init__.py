"""
Market Intelligence Graph Layer

ROLE:
- knowledge representation
- metadata enrichment
- offline analysis

FORBIDDEN:
- runtime execution
- pipeline orchestration
- engine replacement
"""


from .integration import GraphIntegration


__all__ = [
    "GraphIntegration",
]
