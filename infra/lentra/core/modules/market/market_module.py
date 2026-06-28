
from lentra.core.ai.semantic_search.embeddings.embedding_engine import embed
from lentra.core.ai.semantic_search.vector_store.vector_store import search

from lentra.core.market_intelligence.builders.market_object_builder import MarketObjectBuilder
from lentra.core.market_intelligence.pricing.market_price_engine import MarketPriceEngine
from lentra.core.market_intelligence.risk.market_risk_engine import MarketRiskEngine
from lentra.core.market_intelligence.area.area_score_engine import AreaScoreEngine
from lentra.core.market_intelligence.negotiation.negotiation_engine import NegotiationEngine
from lentra.core.market_intelligence.verdict.verdict_engine import VerdictEngine
from lentra.core.market_intelligence.duplicate.duplicate_engine import DuplicateEngine
from lentra.core.market_intelligence.models.market_snapshot import MarketSnapshot


class MarketModule:

    def __init__(self):

        self.builder = MarketObjectBuilder()
        self.pricing = MarketPriceEngine()
        self.risk = MarketRiskEngine()
        self.area = AreaScoreEngine()
        self.negotiation = NegotiationEngine()
        self.verdict = VerdictEngine()
        self.duplicate = DuplicateEngine()

    def run(self, ctx):

        # 🔥 HARD CONTRACT SAFETY
        if isinstance(ctx, dict):

            raise TypeError(
                "PipelineContext expected object, got dict. "
                "Fix PipelineContext initialization."
            )

        query = getattr(ctx, "title", "")

        query_vector = embed(query)

        raw_results = search(query_vector)

        market_objects = []

        for item in raw_results:

            obj = self.builder.build(item)

            obj = self.pricing.run(obj)
            obj = self.risk.run(obj)
            obj = self.area.run(obj)
            obj = self.negotiation.run(obj)
            obj = self.verdict.run(obj)

            market_objects.append(obj)

        market_objects = self.duplicate.run(market_objects)

        snapshot = MarketSnapshot(
            query=query,
            objects=market_objects
        ).finalize()

        ctx.snapshot = snapshot

        return ctx
