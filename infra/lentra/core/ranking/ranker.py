
def rank_listings(listings):
    return sorted(listings, key=lambda x: x.get("risk_score", 1.0))
