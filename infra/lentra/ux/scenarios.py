from lentra.domain.vietnam.adapter import get_vietnam_properties


def run_scenario(intent, payload, state):

    if intent == "property_search":
        props = get_vietnam_properties(payload, state)

        cards = []
        for p in props:
            cards.append({
                "title": p["title"],
                "price": p["price"],
                "location": p["location"]
            })

        return {
            "text": "Нашёл варианты недвижимости:",
            "type": "cards",
            "cards": cards
        }

    if intent == "chat":
        return {
            "text": "Готов помочь с арендой во Вьетнаме.",
            "type": "text"
        }

    return {
        "text": "Запрос обработан",
        "type": "text"
    }
