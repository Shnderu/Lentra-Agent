class BaseHandler:
    """
    Minimal production-safe handler contract.
    """

    def handle(self, task_id: int, payload: dict):
        raise NotImplementedError("Handler must implement handle()")
