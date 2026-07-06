class GraphSelector:
    """
    Stateless selector bound to immutable GraphIndex.
    """

    def __init__(self, index):
        self.index = index

    def select(self, query: str):
        # deterministic routing rules only

        if "risk" in query:
            return ["risk_engine"]

        if "duplicate" in query:
            return ["dedup_engine"]

        if "studio" in query or "beach" in query:
            return ["area_engine"]

        return []
