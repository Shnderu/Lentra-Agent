import threading


class SourceExecutor:

    def __init__(self, service):
        self.service = service

    def run(self, payload: dict) -> dict:
        # V3: sequential-safe placeholder for future parallelism
        return self.service.search(payload)
