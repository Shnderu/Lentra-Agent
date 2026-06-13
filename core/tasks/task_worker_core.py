import json


class TaskWorkerCore:

    def __init__(self, repository):
        self.repo = repository

    def process_batch(self, handler_map: dict, limit: int = 10):

        tasks = self.repo.claim_tasks(limit)

        results = []

        for task_id, task_type, payload in tasks:

            try:
                if isinstance(payload, str):
                    payload = json.loads(payload)

                handler = handler_map.get(task_type)

                if not handler:
                    raise Exception(f"No handler for type: {task_type}")

                result = handler(payload)

                self.repo.mark_done(task_id, result)

                results.append((task_id, "done"))

            except Exception as e:
                self.repo.mark_failed(task_id, str(e))
                results.append((task_id, "failed"))

        return results
