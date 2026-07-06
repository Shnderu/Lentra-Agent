import uuid


class TaskService:

    def create_task(self, task_type: str, payload: dict) -> dict:
        """
        Task ingestion layer (API)
        """

        task_id = str(uuid.uuid4())
        trace_id = str(uuid.uuid4())

        return {
            "task_id": task_id,
            "type": task_type,
            "payload": payload,
            "trace_id": trace_id
        }
