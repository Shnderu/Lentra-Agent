from typing import List
from app.core.ranking.advanced_ranker import AdvancedRanker
from app.core.quality.data_pipeline import DataPipeline
from app.core.ux.response_builder import ResponseBuilder
from app.core.contracts.api_response import APIResponse


class RentAggregator:

    def __init__(self):
        self.ranker = AdvancedRanker()
        self.pipeline = DataPipeline()
        self.builder = ResponseBuilder()

    def aggregate(self, trace_id: str, query: str, sources: List[List], session=None, options=None):

        flat = []
        for source in sources:
            flat.extend(source)

        # -------------------------
        # DATA QUALITY
        # -------------------------
        flat = self.pipeline.process(flat)

        # -------------------------
        # RANKING
        # -------------------------
        if session:
            flat = self.ranker.rank(flat, session)
        else:
            flat.sort(key=lambda x: x.price or 10**9)

        # -------------------------
        # UX RESPONSE BUILD
        # -------------------------
        return self.builder.build(
            trace_id,
            query,
            flat,
            len(flat)
        )
