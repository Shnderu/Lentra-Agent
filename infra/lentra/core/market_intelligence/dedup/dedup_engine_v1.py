class DedupEngineV1:
    """
    Removes duplicate listings and merges near-identical objects.
    """

    def dedup(self, cards: list):

        seen = []
        unique = []

        for c in cards:

            key = (
                str(c.get("price")),
                str(c.get("location")),
                str(c.get("micro_market")),
            )

            if key in seen:
                continue

            seen.append(key)
            unique.append(c)

        return unique
