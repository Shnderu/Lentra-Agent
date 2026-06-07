def fallback_handler(task: dict):
    """
    Safe fallback: never crashes worker.
    """

    print(f"[FALLBACK] No handler for type={task.get('task_type')}, task_id={task.get('id')}")

    return {
        "status": "skipped",
        "reason": "no_handler"
    }
