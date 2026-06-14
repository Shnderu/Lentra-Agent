def map_intent_to_task(intent: str, user_id: int, payload: dict):

    if intent == "FILTER_INTENT":
        return {
            "task_type": "ranking_event",
            "payload": {
                "source": "intent_filter",
                "user_id": user_id
            }
        }

    if intent == "REFINE_INTENT":
        return {
            "task_type": "parse_property",
            "payload": {
                "source": "intent_refine",
                "user_id": user_id
            }
        }

    if intent == "BROWSE_INTENT":
        return {
            "task_type": "ranking_event",
            "payload": {
                "source": "intent_browse",
                "user_id": user_id
            }
        }

    return {
        "task_type": "telegram_message",
        "payload": {
            "source": "intent_default"
        }
    }
