STREAM_MAP = {
    "rent.search": "stream:rent:tasks",
    "flight.search": "stream:flight:tasks",
    "alert": "stream:alerts",
}


class TaskRouter:
    def route(self, task_type: str) -> str:
        return STREAM_MAP.get(task_type, "stream:default")
