from lentra.storage.db import get_conn


def load_profile(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT budget_min, budget_max, preferred_cities, style
        FROM user_profile
        WHERE user_id = %s
    """, (user_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return {
            "budget_min": 0,
            "budget_max": 1000,
            "preferred_cities": [],
            "style": "balanced"
        }

    return {
        "budget_min": row[0],
        "budget_max": row[1],
        "preferred_cities": row[2] or [],
        "style": row[3]
    }


def apply_personalization(properties, profile):
    """
    modifies ranking signal inputs
    """

    for p in properties:
        boost = 0

        price = p.get("price", 0)

        if profile["budget_min"] <= price <= profile["budget_max"]:
            boost += 0.4

        if p.get("city") in profile["preferred_cities"]:
            boost += 0.5

        if profile["style"] == "budget" and price < 400:
            boost += 0.3

        p["personal_score"] = boost

    return properties
