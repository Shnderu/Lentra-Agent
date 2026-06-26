"""
GRAPH MODULE IS ISOLATED

STRICT RULE:
- NO imports from graph allowed in:
  pipeline
  executor
  scenario
"""

def get_graph_engine():
    from .engine import GraphEngine
    return GraphEngine()
