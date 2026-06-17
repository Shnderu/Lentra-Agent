from typing import List
from app.core.contracts.response_dto import RentResponseDTO
from app.core.ranking.advanced_ranker import AdvancedRanker
from app.core.quality.data_pipeline import DataPipeline
from app.core.ux.result_formatter import ResultFormatter


class RentAggregator:

    def __init__(self):
        self.ranker = AdvancedRanker()
        self.pipeline = DataPipeline()
        self.formatter = ResultFormatter()

    def aggregate(self, query: str, sources: List[List], session=None, options=None):

        flat = []
        for source in sources:
            flat.extend(source)

        # -------------------------
        # DATA QUALITY LAYER
        # -------------------------
        flat = self.pipeline.process(flat)

        # -------------------------
        # RANKING
        # -------------------------
        if session:
            flat = self.ranker.rank(flat, session)
        else:
            flat.sort(key=lambda x: x.price or 10**9)

        response = RentResponseDTO(
            query=query,
            listings=flat,
            total=len(flat)
        )

        # -------------------------
        # UX LAYER (NEW)
        # -------------------------
        if options:
            return self.formatter.format(response, options)

        return response
