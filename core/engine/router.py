from typing import Dict, Any, Callable


class TaskRouter:
    def __init__(self):
        self._handlers: Dict[str, Callable] = {}

    def register(self, task_type: str):
        def wrapper(fn: Callable):
            self._handlers[task_type] = fn
            return fn
        return wrapper

    def resolve(self, task_type: str) -> Callable:
        return self._handlers.get(task_type, self._default_handler)

    def _default_handler(self, conn, task: Dict[str, Any]):
        print(f"[ROUTER] No handler for type={task.get('task_type')}")
        return None


router = TaskRouter()
