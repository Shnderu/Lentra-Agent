from lentra.bot.core.intent_classifier import IntentClassifier


class IntentResolver:
    def __init__(self, feature_registry):
        self.feature_registry = feature_registry
        self.classifier = IntentClassifier()

    def resolve(self, text: str):
        intent = self.classifier.classify(text)
        return self.feature_registry.get(intent)
