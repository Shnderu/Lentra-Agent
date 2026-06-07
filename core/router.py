from core.handlers.test import handle_test


HANDLERS = {
    "test": handle_test,
}


def route_task(task: dict, conn):
    task_type = task.get("task_type")

    handler = HANDLERS.get(task_type)

    if not handler:
        print(f"[ROUTER] No handler for type={task_type}")
        return None

    return handler(task, conn)
