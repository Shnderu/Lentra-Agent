class Registry:
    """
    CENTRAL DI REGISTRY (LOCKED CORE LAYER)
    """

    def __init__(self):
        self._services = {}

    def register(self, name: str, obj):
        self._services[name] = obj

    def resolve(self, name: str):
        return self._services.get(name)

    def execute(self, intent: str, context: dict):
        handler = self._services.get("handler")
        if not handler:
            raise RuntimeError("Handler not registered in registry")
        return handler(intent, context)


def build_registry():
    return Registry()
