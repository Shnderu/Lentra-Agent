def build_intent_resolver(registry):
    """
    LOCK LEVEL 3: intent resolution layer
    """
    return registry.get("intent_resolver")
