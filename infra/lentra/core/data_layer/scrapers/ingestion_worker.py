from lentra.workers.base_worker import BaseWorker


class IngestionWorker(BaseWorker):
    """
    DATA INGESTION = NO CORE LOGIC ACCESS

    ONLY:
    ingest → executor → pipeline
    """

    def ingest(self, raw_data: dict):
        task = {
            "type": "ingestion",
            "payload": raw_data
        }

        return self.handle(task)
