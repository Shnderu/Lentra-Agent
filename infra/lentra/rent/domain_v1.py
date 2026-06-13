# ============================================================
# PATCH V16.2 - REAL CONNECTORS INTEGRATION
# ============================================================

from lentra.rent.connector_engine import ConnectorEngine
from lentra.rent.connectors.airbnb_connector import AirbnbConnector
from lentra.rent.connectors.local_connector import LocalMarketConnector
from lentra.rent.connectors.scraper_connector import ScraperConnector

from lentra.rent.normalization_engine import NormalizationEngine
from lentra.rent.normalizers.airbnb import AirbnbNormalizer
from lentra.rent.normalizers.local import LocalNormalizer
from lentra.rent.normalizers.scraper import ScraperNormalizer

from lentra.rent.search_pipeline import run_search_pipeline_canonical


class SearchRentHandler:
    def __init__(self):
        self.connector_engine = ConnectorEngine([
            AirbnbConnector(),
            LocalMarketConnector(),
            ScraperConnector(),
        ])

        self.normalizer = NormalizationEngine([
            AirbnbNormalizer(),
            LocalNormalizer(),
            ScraperNormalizer(),
        ])

    async def handle(self, task):
        payload = task.get("payload", {})

        validate_rent_payload(payload)

        raw = await self.connector_engine.fetch_all(payload)

        normalized = self.normalizer.normalize_batch(raw)

        results = run_search_pipeline_canonical(normalized, payload)

        return {
            "task_id": task["id"],
            "status": "success",
            "results": results,
            "mode": "v16.2_real_connectors",
        }
