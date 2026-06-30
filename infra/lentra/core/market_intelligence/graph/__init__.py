"""
Graph package stabilized entrypoint
Avoid direct engine import on module load
"""

def get_market_graph_engine():
    from .market_graph_engine import MarketGraphEngine
    return MarketGraphEngine
