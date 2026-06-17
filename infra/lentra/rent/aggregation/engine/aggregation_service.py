from lentra.rent.aggregation.engine.merge_engine import MergeEngine
from lentra.rent.ranking.engine.ranking_engine import RankingEngine


class AggregationService:

    def __init__(self, registry):
        self.registry = registry
        self.merger = MergeEngine()
        self.ranker = RankingEngine()

    async def search(self, query: dict) -> dict:

        raw_results = await self.registry.fanout(query)

        merged = self.merger.merge(raw_results)

        ranked = self.ranker.rank(merged, query)

        top_k = ranked[:10]

        return {
            "source": "aggregation_engine_v7",
            "items": top_k,
            "sources_count": len(raw_results)
        }
