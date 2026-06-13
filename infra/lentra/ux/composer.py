def compose_response(scenario_result):
    """
    Превращает UX сценарий в Telegram-ready формат
    """

    if scenario_result["type"] == "text":
        return {
            "telegram": {
                "text": scenario_result["text"]
            }
        }

    if scenario_result["type"] == "cards":
        return {
            "telegram": {
                "text": scenario_result["text"],
                "cards": scenario_result.get("cards", [])
            }
        }

    return {
        "telegram": {
            "text": "OK"
        }
    }
