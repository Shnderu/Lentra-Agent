

from collections import defaultdict
from lentra.core.ai.semantic_search.embeddings.embedding_engine import embed


def cosine_sim(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    norm_a = sum(x*x for x in a) ** 0.5
    norm_b = sum(x*x for x in b) ** 0.5
    return dot / (norm_a * norm_b + 1e-8)


class DedupEngine:

    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold

    def cluster(self, listings: list):

        clusters = []

        for listing in listings:

            emb = embed(listing.get("title", ""))

            placed = False

            for cluster in clusters:

                # compare with first item of cluster
                base = cluster["embedding"]

                if cosine_sim(emb, base) >= self.threshold:
                    cluster["items"].append(listing)
                    placed = True
                    break

            if not placed:
                clusters.append({
                    "embedding": emb,
                    "items": [listing]
                })

        # convert to dict format
        result = {}

        for i, c in enumerate(clusters):
            result[f"cluster_{i}"] = c["items"]

        return result
