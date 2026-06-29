class DecisionNarrativeEngine:
    """
    Converts market signals into human decision explanation.
    """

    def explain(self, listing: dict):

        verdict = listing.get("verdict")
        risk = listing.get("risk") or 0.5

        parts = []

        if verdict == "overpriced":
            parts.append("Цена выше рыночного уровня")
        elif verdict == "cheap":
            parts.append("Цена ниже рыночного уровня")
        else:
            parts.append("Цена соответствует рынку")

        if risk > 0.75:
            parts.append("высокий риск")
        elif risk < 0.3:
            parts.append("низкий риск")

        listing["explanation"] = " • ".join(parts[:3])

        return listing
