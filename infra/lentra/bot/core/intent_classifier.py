import re
from typing import Optional


class IntentClassifier:
    """
    Rule-based intent classifier.
    Без AI. Только deterministic routing.
    """

    def classify(self, text: str) -> str:
        if not text:
            return "fallback"

        text = text.lower()

        # SEARCH INTENT
        if re.search(r"(rent|buy|property|flat|house|apartment|аренда|жилье)", text):
            return "search"

        # PROFILE INTENT (заготовка под будущее)
        if re.search(r"(profile|account|me|профиль|аккаунт)", text):
            return "profile"

        # DEFAULT
        return "search"
