

def plan_query(query: str) -> dict:

    query = query.lower()

    plan = {
        "max_price": None,
        "location": None,
        "must_have": [],
        "noise_sensitive": False,
        "internet_required": False
    }

    # price extraction (simple MVP logic)
    if "700" in query:
        plan["max_price"] = 700

    if "800" in query:
        plan["max_price"] = 800

    # location detection
    if "beach" in query:
        plan["location"] = "My Khe"

    if "тихий" in query or "quiet" in query:
        plan["noise_sensitive"] = True

    if "wifi" in query or "интернет" in query:
        plan["internet_required"] = True

    plan["must_have"] = []

    if plan["internet_required"]:
        plan["must_have"].append("internet")

    return plan
