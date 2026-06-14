def execute_task(task_type, payload):
    if task_type == "telegram_message":
        data = payload.get("data", {})
        text = data.get("text", "")

        if text == "/start":
            return {
                "text": "Главное меню готово",
                "reply_markup": {
                    "keyboard": [
                        ["🏠 Аренда", "🔍 Поиск"],
                        ["👤 Профиль", "⚙️ Настройки"]
                    ],
                    "resize_keyboard": True
                }
            }

        return {"text": "Неизвестный сценарий"}

    return {"text": "unsupported task type"}
