def normalize(text: str) -> str:
    return text.lower().strip()


def classify(text: str, source="message"):
    text = normalize(text)

    # -------------------------
    # ROUTE SEARCH
    # -------------------------
    if any(x in text for x in ["flight", "рейс", "самара", "куда", "лететь"]):
        return Intent(name="route_search", confidence=0.9)

    # -------------------------
    # DEAL SEARCH
    # -------------------------
    if any(x in text for x in ["deal", "скидка", "горящие", "дешево"]):
        return Intent(name="deal_search", confidence=0.85)

    # -------------------------
    # WATCH ROUTE
    # -------------------------
    if any(x in text for x in ["следить", "мониторинг", "цена", "уведомление"]):
        return Intent(name="watch_route", confidence=0.85)

    # -------------------------
    # AI PLANNER
    # -------------------------
    if len(text.split()) > 4:
        return Intent(name="ai_planner", confidence=0.7)

    # -------------------------
    # FALLBACK (NO HACK RESPONSE)
    # -------------------------
    return Intent(name="unknown", confidence=0.1)
