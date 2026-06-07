from core.router.registry import HANDLERS


class TaskRouterV2:
    def __init__(self):
        self.handlers = HANDLERS

    def route(self, task: dict):
        task_type = task["task_type"]

        if task_type not in self.handlers:
            raise ValueError(f"No handler registered for task_type={task_type}")

        handler = self.handlers[task_type]
        return handler(task)
