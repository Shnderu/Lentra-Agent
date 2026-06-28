def parse_query(query: str):
    """
    Minimal MVP parser for search queries
    """
    if not query:
        return {}

    tokens = query.lower().split()

    parsed = {
        "raw": query,
        "tokens": tokens,
        "budget": None,
        "keywords": tokens,
        "city": None,
        "noise_sensitive": False,
        "internet_required": False,
    }

    # very simple heuristics (MVP)
    for i, t in enumerate(tokens):
        if t in ["under", "below", "до"]:
            if i + 1 < len(tokens):
                parsed["budget"] = tokens[i + 1]

        if t in ["quiet", "low-noise", "тихо"]:
            parsed["noise_sensitive"] = True

        if t in ["internet", "wifi"]:
            parsed["internet_required"] = True

    return parsed
