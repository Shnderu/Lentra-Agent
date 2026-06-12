class CostOptimizer:
    """
    Reduces external calls based on heuristics.
    """

    def should_skip(self, task: dict) -> bool:
        payload = task.get("payload", {})

        if isinstance(payload, str):
            return False

        city = payload.get("city", "")

        # simple heuristic (extend later)
        if city.lower() in ["unknown", "test"]:
            return True

        return False
