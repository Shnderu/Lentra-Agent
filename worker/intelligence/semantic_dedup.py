import numpy as np
from numpy.linalg import norm

def cosine(a, b):
    return float(np.dot(a, b) / (norm(a) * norm(b) + 1e-9))


def deduplicate(items: list, embeddings: list, threshold: float = 0.88):
    unique_items = []
    unique_embs = []

    for item, emb in zip(items, embeddings):

        is_dup = False

        for u_emb in unique_embs:
            if cosine(emb, u_emb) > threshold:
                is_dup = True
                break

        if not is_dup:
            unique_items.append(item)
            unique_embs.append(emb)

    return unique_items, unique_embs
