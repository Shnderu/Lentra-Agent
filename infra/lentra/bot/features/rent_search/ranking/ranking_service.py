# ============================================================
# RENT RANKING SERVICE V1 - SAFE DETERMINISTIC
# ============================================================

class RankingService:
    """
    Safe ranking engine without external execution.
    """

    def rank(self, items):
        if not isinstance(items, list):
            return []

        return sorted(
            items,
            key=lambda x: x.get("score", 0) if isinstance(x, dict) else 0,
            reverse=True
        )
