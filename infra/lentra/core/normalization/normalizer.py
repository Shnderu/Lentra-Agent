
def normalize(listings):
    normalized = []

    for l in listings:
        l["normalized_price"] = float(l["price"])
        normalized.append(l)

    return normalized
