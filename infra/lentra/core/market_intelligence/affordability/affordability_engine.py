class AffordabilityEngine:
    """
    Evaluates whether listing is financially safe for expats.
    """

    def evaluate(self, listing: dict, income: float = 2000):

        price = listing.get("price") or 0

        ratio = price / income if income else 1

        if ratio < 0.25:
            level = "safe"
        elif ratio < 0.4:
            level = "moderate"
        else:
            level = "high_risk"

        return {
            "affordability_ratio": round(ratio, 3),
            "affordability_level": level,
            "recommended_budget_max": round(income * 0.3, 2)
        }
