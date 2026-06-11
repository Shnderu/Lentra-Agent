from typing import List

from core.domain import RentQuery, RentListing, RentResult
from core.ingestion.facebook import FacebookIngestion
from core.ingestion.faswaz import FaswazIngestion


class IngestionPipeline:

    def __init__(self):
        self.sources = [
            FacebookIngestion(),
            FaswazIngestion()
        ]

    def run(self, query: RentQuery) -> RentResult:
        listings: List[RentListing] = []
        used = []

        for source in self.sources:
            try:
                items = source.fetch(query)
                listings.extend(items)
                used.append(source.name)
            except Exception:
                continue

        return RentResult(
            listings=listings,
            sources_used=used,
            raw={"pipeline": "ingestion_v1"}
        )
