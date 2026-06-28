

def rank_listings(listings, plan, user_id=None):

    scored = []

    for l in listings:

        score = 0

        # PRICE CHECK
        if plan.get("max_price") and l.get("price") <= plan["max_price"]:
            score += 50

        # INTERNET CHECK (FIXED SEMANTIC MATCH)
        if plan.get("internet_required"):
            if "internet" in l.get("features", []):
                score += 50
            else:
                continue

        scored.append((score, l))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [x[1] for x in scored]
