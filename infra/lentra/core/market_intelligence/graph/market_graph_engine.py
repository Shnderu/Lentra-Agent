from lentra.core.market_intelligence.graph.graph_registry import GraphRegistry


class MarketGraphEngine:

    """
    Frozen graph definition.
    No runtime mutation allowed.
    """

    def __init__(self):
        self.registry = GraphRegistry()

    def register_engine(self, name, engine):
        self.registry.register(name, engine)

    def get_engine(self, name):
        return self.registry.get(name)

    def snapshot(self):
        return self.registry.all()
