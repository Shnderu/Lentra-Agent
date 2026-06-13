def search_vietnam_properties(payload: dict):
    # REAL INPUT NOW (not text query)

    price = payload.get("price", 0)
    title = payload.get("title", "")

    return {
        "matched": True,
        "title": title,
        "analysis": {
            "affordability": "good" if price < 500 else "high",
            "recommendation_score": 0.9 if price < 500 else 0.6
        }
    }
