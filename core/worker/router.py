from core.worker.handlers.send_message import SendMessageHandler
from core.worker.handlers.notify import NotifyHandler


class TaskRouter:

    def __init__(self):
        self.handlers = {
            "send_message": SendMessageHandler(),
            "notify": NotifyHandler(),
        }

    async def route(self, task: dict):
        task_id = task["id"]
        task_type = task["type"]
        payload = task.get("payload", {})

        handler = self.handlers.get(task_type)

        if not handler:
            raise ValueError(f"Unknown task type: {task_type}")

        return await handler.handle(task_id, payload)
