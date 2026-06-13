# ============================================================
# NORMALIZER V1
# ============================================================

class Normalizer:

    def transform(self, listings):
        normalized = []

        for l in listings:
            normalized.append({
                "id": l["id"],
                "title": l["title"],
                "price": l.get("price", 0),
                "location_score": l.get("location_score", 0),
                "trust_score": l.get("trust", 0)
            })

        return normalized
