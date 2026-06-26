from lentra.workers.base_worker import BaseWorker


class QueueWorker(BaseWorker):
    """
    Queue worker = execution proxy only
    """

    def process(self, task: dict):
        return self.handle(task)
