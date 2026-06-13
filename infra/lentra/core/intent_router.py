def classify(text: str):
    t = text.lower()

    # VIETNAM RENT CORE (MAIN PRODUCT)
    if any(k in t for k in ["вьетнам", "ho chi minh", "hanoi", "дананг", "аренда", "квартира"]):
        return {
            "task_type": "search_property_vietnam",
            "payload": {
                "raw_query": text
            }
        }

    if "цена" in t:
        return {
            "task_type": "price_alert",
            "payload": {"query": text}
        }

    return {
        "task_type": "ai_summary",
        "payload": {"query": text}
    }
