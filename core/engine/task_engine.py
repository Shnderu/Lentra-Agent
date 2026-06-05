from core.engine.repository import insert_task


class TaskEngine:
    def add_task(self, task_type, payload, retries=3):
        return insert_task(task_type, payload, retries)


engine = TaskEngine()


def add_task(task_type, payload, retries=3):
    return engine.add_task(task_type, payload, retries)
