from lentra.workers.base_worker import BaseWorker


class EventWorker(BaseWorker):
    """
    Event worker = no logic, only forwarding
    """

    def on_event(self, event: dict):
        return self.handle(event)
