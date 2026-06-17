from typing import List
from app.core.quality.data_pipeline import DataPipeline
from app.core.ranking.advanced_ranker import AdvancedRanker


class RentAggregator:

    def __init__(self):
        self.pipeline = DataPipeline()
        self.ranker = AdvancedRanker()

    def aggregate(self, query: str, sources: List[List], session=None):

        flat = []
        for source in sources:
            flat.extend(source)

        # -------------------------
        # DATA QUALITY (CORE)
        # -------------------------
        flat = self.pipeline.process(flat)

        # -------------------------
        # SINGLE RANKING SOURCE OF TRUTH
        # -------------------------
        if session:
            flat = self.ranker.rank(flat, session)
        else:
            flat.sort(key=lambda x: x.price or 10**9)

        return {
            "query": query,
            "listings": flat,
            "total": len(flat)
        }
