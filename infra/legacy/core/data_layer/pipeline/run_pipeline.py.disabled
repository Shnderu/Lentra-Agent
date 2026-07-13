from lentra.core.data_layer.pipeline.ingestion_pipeline import IngestionPipeline
from lentra.core.data_layer.adapters.facebook import FacebookAdapter
from lentra.core.data_layer.adapters.telegram import TelegramAdapter
from lentra.core.data_layer.adapters.local_sites import LocalSitesAdapter
from lentra.core.search.search_engine import SearchEngine


class PipelineRunner:
    """
    VIETNAM FULL SYSTEM RUNNER
    """

    def __init__(self):
        self.pipeline = IngestionPipeline()

        self.search_engine = SearchEngine(self.pipeline)

        self.adapters = [
            FacebookAdapter(),
            TelegramAdapter(),
            LocalSitesAdapter()
        ]

    def run_once(self):
        all_raw = []

        for adapter in self.adapters:
            all_raw.extend(adapter.fetch())

        result = self.pipeline.ingest_batch(all_raw)

        return result

    def search(self, query: dict):
        return self.search_engine.search(query)


if __name__ == "__main__":
    runner = PipelineRunner()
    runner.run_once()

    print(
        runner.search({
            "city": "da nang",
            "max_price": 15000000,
            "max_risk": 70
        })
    )
