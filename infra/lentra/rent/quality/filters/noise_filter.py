# ============================================================
# NOISE FILTER V16.3
# ============================================================

def noise_score(listing: dict) -> float:
    score = 0

    if not listing.get("title"):
        score += 40

    if listing.get("price", 0) <= 0:
        score += 50

    if len(listing.get("title", "")) < 10:
        score += 20

    return min(score, 100)
