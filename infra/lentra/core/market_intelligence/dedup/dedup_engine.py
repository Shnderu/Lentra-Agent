class DedupEngine:

    def cluster(self, listings):

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

                if self._similar(item, other):
                    cluster.append(other)
                    used.add(j)

            clusters.append({
                "listings": cluster
            })

        return clusters

    def _similar(self, a, b):

        if (a.get("title") or "").lower() == (b.get("title") or "").lower():
            return True

        pa = a.get("price")
        pb = b.get("price")

        if pa and pb:
            return abs(pa - pb) / max(pa, pb) < 0.1

        return False
