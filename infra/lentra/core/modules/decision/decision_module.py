
from lentra.core.market_intelligence.decision.ranking_engine import RankingEngine


class DecisionModule:

    def __init__(self):
        self.engine = RankingEngine()

    def run(self, ctx):

        if not hasattr(ctx, "search_results"):
            return ctx

        # 🔥 ГАРАНТИЯ: всегда enrich BEFORE UI
        ranked = self.engine.run(ctx.search_results)

        for obj in ranked:

            if not hasattr(obj, "final_score"):
                obj.final_score = 0.0

            # 🔥 HARD GUARANTEE CONTRACT
            obj.confidence = getattr(obj, "confidence", 0.5)

        ctx.search_results = ranked

        return ctx

