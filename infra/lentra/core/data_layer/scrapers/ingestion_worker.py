
from lentra.core.queue.task_repository import TaskRepository
from lentra.core.data_layer.sources.facebook import FacebookSource
from lentra.core.data_layer.builders.task_builder import TaskBuilder


class IngestionWorker:

    def __init__(self):
        self.repo = TaskRepository("postgresql://lentra:lentra@localhost:5432/lentra")
        self.source = FacebookSource()
        self.builder = TaskBuilder()

    def run(self):

        print("[INGESTION] START")

        listings = self.source.fetch()

        for l in listings:

            task = self.builder.build(l)

            task_id = self.repo.push(task)

            print("[INGESTED]", task_id, task)

