def execute_task(task_type, payload):
    handler = HANDLERS.get(task_type)

    if not handler:
        return {
            "ux": {"screen": "error"},
            "telegram_text": f"UNKNOWN_TASK_TYPE:{task_type}"
        }

    state = {}

    try:
        result = handler(payload, state)

        # 🔥 HARD GUARANTEE CONTRACT
        if result is None:
            return {
                "ux": {"screen": "empty"},
                "telegram_text": "EMPTY_RESULT"
            }

        if not isinstance(result, dict):
            return {
                "ux": {"screen": "error"},
                "telegram_text": str(result)
            }

        return result

    except Exception as e:
        return {
            "ux": {"screen": "error"},
            "telegram_text": f"EXEC_ERROR:{str(e)}"
        }
