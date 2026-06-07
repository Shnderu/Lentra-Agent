def handle_test(task: dict, conn):
    payload = task.get("payload", {})

    print(f"[HANDLER:test] payload={payload}")

    # бизнес-логика теста
    return {
        "ok": True,
        "task_id": task.get("id"),
    }
