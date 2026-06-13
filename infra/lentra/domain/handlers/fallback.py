def handle_unknown(task_type, payload):
    return {
        "ux": {
            "screen": "error",
            "title": "Unknown task type",
            "task_type": task_type,
            "payload": payload
        },
        "telegram_text": f"⚠️ Unknown task: {task_type}"
    }
