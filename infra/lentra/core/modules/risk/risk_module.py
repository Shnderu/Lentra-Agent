
from lentra.core.market_intelligence.risk.antiscam.antiscam_engine import AntiScamEngine


class RiskModule:

    def __init__(self):
        self.engine = AntiScamEngine()

    def run(self, ctx):

        risks = []

        for item in ctx.search_results:

            result = self.engine.score(item, {})
            risks.append(result.get("scam_score", 0.5))

        # агрегируем в SCALAR
        ctx.risk = sum(risks) / len(risks) if risks else 0.5

        return ctx
