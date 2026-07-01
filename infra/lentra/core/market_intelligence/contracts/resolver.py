from lentra.core.market_intelligence.contracts.routing_map import RoutingMap


class EngineResolver:
    """
    Lightweight dependency resolver.
    NO architecture, only mapping → instance binding.
    """

    def __init__(self):
        self.routing = RoutingMap()

    def resolve_pricing(self, cls):
        return cls()

    def resolve_dedup(self, cls):
        return cls()

    def resolve_risk(self, cls):
        return cls()

    def resolve_expat(self, cls):
        return cls()
