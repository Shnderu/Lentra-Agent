from core.handlers.test import handle_test


class TaskRouter:
    def __init__(self):
        self.registry = {
            "test": handle_test,
        }

    def route(self, task_type: str, payload: dict):
        if task_type not in self.registry:
            raise ValueError(f"No handler registered for task_type={task_type}")

        return self.registry[task_type](payload)
