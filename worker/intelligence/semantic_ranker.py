import numpy as np
from numpy.linalg import norm


def cosine(a, b):
    return float(np.dot(a, b) / (norm(a) * norm(b) + 1e-9))


def rank(items, item_embs, query_emb):

    scored = []

    for item, emb in zip(items, item_embs):

        semantic_score = cosine(query_emb, emb)

        price = item.get("price", 0) or 0
        price_score = 1 / (1 + price / 1000)

        source_score = {
            "facebook": 0.7,
            "faswaz": 0.9
        }.get(item.get("source"), 0.5)

        final = (
            semantic_score * 0.6 +
            price_score * 0.2 +
            source_score * 0.2
        )

        item["score"] = round(final, 4)
        scored.append(item)

    return sorted(scored, key=lambda x: x["score"], reverse=True)
