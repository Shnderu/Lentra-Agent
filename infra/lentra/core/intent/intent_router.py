def build_intent_router(registry):
    return IntentRouter(registry)


class IntentRouter:
    def __init__(self, registry):
        self.registry = registry

    def get_feature(self, intent):
        return self.registry.get(intent)
