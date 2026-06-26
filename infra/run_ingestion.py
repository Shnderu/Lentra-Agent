
from lentra.core.data_layer.scrapers.ingestion_worker import IngestionWorker


if __name__ == "__main__":
    worker = IngestionWorker()
    worker.run()
