class Registry:
    """
    CENTRAL DI REGISTRY (STABLE ADAPTER MODE)
    """

    def __init__(self):
        self._services = {}

    def register(self, name: str, obj):
        self._services[name] = obj

    def resolve(self, name: str):
        return self._services.get(name)

    # COMPAT LAYER (CRITICAL FIX)
    def classify(self, text: str):
        classifier = self._services.get("intent_classifier")
        if classifier and hasattr(classifier, "classify"):
            return classifier.classify(text)
        if callable(classifier):
            return classifier(text)
        return {"type": "unknown", "confidence": 0.0, "payload": text}

    def execute(self, intent: str, context: dict):
        handler = self._services.get("handler")
        if not handler:
            raise RuntimeError("Handler not registered in registry")
        return handler(intent, context)


def build_registry():
    return Registry()
