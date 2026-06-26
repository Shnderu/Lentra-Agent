class IntentResolver:
    def __init__(self, registry):
        self.registry = registry

    def resolve(self, text: str):
        return self.registry.classify(text)


def build_intent_resolver(registry):
    return IntentResolver(registry)
