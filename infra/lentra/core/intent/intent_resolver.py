from lentra.core.contracts.v1 import IntentV1
from lentra.core.intent.intent_classifier import IntentClassifier


class IntentResolver:
    """
    CORE v1.1 — строго IntentV1 output
    """

    def __init__(self):
        self.classifier = IntentClassifier()

    def resolve(self, flow) -> IntentV1:
        raw = self.classifier.classify(flow.text)

        return IntentV1(
            type=raw.get("type", "unknown"),
            confidence=raw.get("confidence", 0.0),
            raw=raw
        )
