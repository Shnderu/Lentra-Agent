import asyncio
from core.domain import RentQuery
from core.ingestion.pipeline.engine import IngestionEngine


class RentCoreService:

    def __init__(self):
        self.engine = IngestionEngine()

    def search(self, query: RentQuery):
        return asyncio.run(self.engine.run(query))
