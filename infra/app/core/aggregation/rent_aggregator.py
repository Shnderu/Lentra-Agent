from typing import List
from app.core.contracts.response_dto import RentResponseDTO
from app.core.ranking.advanced_ranker import AdvancedRanker
from app.core.quality.data_pipeline import DataPipeline


class RentAggregator:

    def __init__(self):
        self.ranker = AdvancedRanker()
        self.pipeline = DataPipeline()

    def aggregate(self, query: str, sources: List[List], session=None):

        flat = []
        for source in sources:
            flat.extend(source)

        # 🔥 DATA QUALITY LAYER (NEW)
        flat = self.pipeline.process(flat)

        # ranking input
        if session:
            flat = self.ranker.rank(flat, session)
        else:
            flat.sort(key=lambda x: x.price or 10**9)

        return RentResponseDTO(
            query=query,
            listings=flat,
            total=len(flat)
        )
