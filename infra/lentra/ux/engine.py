def resolve_intent(task_type, payload):
    """
    UX LAYER v1
    превращает task → смысл
    """

    if task_type == "telegram_message":
        return {
            "intent": "chat",
            "scenario": "basic_reply"
        }

    if task_type == "parse_property":
        return {
            "intent": "property_search",
            "scenario": "list_properties"
        }

    if task_type == "ranking_event":
        return {
            "intent": "analytics",
            "scenario": "ranking_report"
        }

    return {
        "intent": "unknown",
        "scenario": "fallback"
    }


def build_response(intent_data, payload):
    """
    UX response builder
    """

    scenario = intent_data["scenario"]

    if scenario == "basic_reply":
        return {"text": "Message received and processed."}

    if scenario == "list_properties":
        return {
            "text": "Found relevant properties for your request.",
            "cards": []
        }

    if scenario == "ranking_report":
        return {
            "text": "Ranking completed successfully.",
            "metrics": {}
        }

    return {"text": "Request processed."}
