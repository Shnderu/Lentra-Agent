"""
GRAPH MODULE IS ISOLATED

STRICT RULE:
- NO imports from graph allowed in:
  pipeline
  executor
  scenario

Graph is offline compiler only.
"""


def get_graph_compiler():
    from .engine import OfflineGraphCompiler

    return OfflineGraphCompiler()
