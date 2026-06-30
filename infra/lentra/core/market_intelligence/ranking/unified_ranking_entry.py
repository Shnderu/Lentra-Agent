class UnifiedRankingEntry:

    def __init__(self, engines: dict):
        self.engines = engines

    def rank(self, items, context=None):

        # deterministic execution order
        base = self.engines["base"].rank(items, context)

        enriched = self.engines["ensemble"].rank(base, context)

        return self.engines["adaptive"].rank(enriched, context)
