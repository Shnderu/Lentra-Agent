def build_property_card(p):
    return {
        "type": "card",
        "title": p.get("title", "Property"),
        "price": p.get("price"),
        "city": p.get("city"),
        "meta": {
            "score": p.get("rank_score", 0),
            "why": p.get("reason", "best match")
        }
    }


def compose_properties(properties):
    cards = []

    for p in properties:
        cards.append(build_property_card(p))

    return {
        "screen": "property_list",
        "title": "Подобрано для тебя",
        "cards": cards,
        "actions": [
            {"type": "filter", "label": "Фильтры"},
            {"type": "refine", "label": "Уточнить"}
        ]
    }
