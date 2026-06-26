from lentra.core.executor import get_executor


class BaseWorker:
    """
    SINGLE RULE:
    Workers НЕ имеют права вызывать core напрямую.

    Единственный путь:
    worker → executor → pipeline
    """

    def __init__(self, pipeline=None):
        self.executor = get_executor(pipeline)

    def handle(self, task: dict):
        return self.executor.execute(task=task)
