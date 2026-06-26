def build_intent_router(registry):
    """
    LOCK LEVEL 3: single intent routing entrypoint
    """
    return registry.get("intent_router")


def classify(text: str):
    return {
        "intent": "unknown",
        "confidence": 0.0,
    }
