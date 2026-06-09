
def build_search(intent):

    if intent.origin and intent.destination:

        return {
            "type": "route_search",
            "payload": {
                "from": intent.origin,
                "to": intent.destination,
                "date": intent.date
            }
        }

    # fallback → deal search
    return {
        "type": "deal_search",
        "payload": {
            "budget": intent.budget
        }
    }
