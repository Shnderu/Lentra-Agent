

class EntityResolutionEngine:

    def similarity(self, a: dict, b: dict):

        score = 0.0

        # title similarity (primitive)
        if a.get("title") and b.get("title"):
            if a["title"].lower() == b["title"].lower():
                score += 0.5

        # price proximity
        pa = a.get("price", 0)
        pb = b.get("price", 0)

        if pa and pb:
            diff = abs(pa - pb) / max(pa, pb)
            score += max(0, 0.3 - diff)

        # location match
        if a.get("location") == b.get("location"):
            score += 0.2

        # source diversity bonus (anti-fake boost)
        if a.get("source") != b.get("source"):
            score += 0.1

        return min(score, 1.0)


    def cluster(self, listings, threshold=0.75):

        clusters = []
        used = set()

        for i, item in enumerate(listings):

            if i in used:
                continue

            cluster = [item]
            used.add(i)

            for j, other in enumerate(listings):

                if j in used:
                    continue

                if self.similarity(item, other) >= threshold:
                    cluster.append(other)
                    used.add(j)

            clusters.append({
                "confidence": sum([self.similarity(item, x) for x in cluster]) / len(cluster),
                "listings": cluster
            })

        return clusters
