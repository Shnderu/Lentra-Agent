class ClusterEngineV1:
    """
    Simple clustering by micro_market + price band.
    """

    def cluster(self, cards: list):

        clusters = {}

        for c in cards:

            market = c.get("micro_market", "unknown")
            price = c.get("price") or 0

            band = int(price // 200) * 200  # price band clustering

            key = f"{market}:{band}"

            if key not in clusters:
                clusters[key] = []

            clusters[key].append(c)

        return list(clusters.values())
