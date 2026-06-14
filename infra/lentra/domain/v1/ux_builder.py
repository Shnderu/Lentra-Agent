def build_property_list(properties):

    cards = []

    for p in properties:

        cards.append({
            "id": p["id"],
            "title": p["title"],
            "subtitle": f'{p["city"]} • ${p["price"]}',
            "score": p.get("rank_score", 0),
            "actions": [
                {
                    "text": "Open",
                    "callback_data": f"open:{p['id']}"
                },
                {
                    "text": "Save",
                    "callback_data": f"save:{p['id']}"
                }
            ]
        })

    return {
        "ux": {
            "screen": "property_list",
            "cards": cards
        }
    }
