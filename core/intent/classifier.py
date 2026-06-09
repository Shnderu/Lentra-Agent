
import re
from core.intent.types import Intent


def classify(text: str, source="message") -> Intent:

    t = text.lower()

    # ROUTE SEARCH
    if "→" in text or "лети" in t:
        return Intent(
            name="route_search",
            confidence=0.9,
            payload={"text": text},
            source=source
        )

    # WATCH ROUTE
    if "следи" in t or "watch" in t:
        return Intent(
            name="watch_route",
            confidence=0.85,
            payload={"text": text},
            source=source
        )

    # DEAL SEARCH
    if "горящ" in t or "deal" in t:
        return Intent(
            name="deal_search",
            confidence=0.8,
            payload={"text": text},
            source=source
        )

    # AI PLANNER
    if len(t.split()) > 5:
        return Intent(
            name="ai_planner",
            confidence=0.75,
            payload={"text": text},
            source=source
        )

    return Intent(
        name="unknown",
        confidence=0.3,
        payload={"text": text},
        source=source
    )
