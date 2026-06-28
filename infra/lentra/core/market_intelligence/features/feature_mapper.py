

def to_feature_vector(listing: dict):

    text = (listing.get("title") or "").lower()

    features = set()

    # INTERNET MAPPING
    if "wifi" in text or "internet" in text or "fiber" in text:
        features.add("internet")

    # BEACH MAPPING
    if "beach" in text or "sea" in text:
        features.add("beach_proximity")

    # NOISE (simple heuristic)
    if "quiet" in text or "calm" in text:
        features.add("low_noise")

    return {
        "features": list(features)
    }
