# ============================================================
# AGENT ACTION EXECUTOR V17.0
# ============================================================


class ActionExecutor:
    def execute(self, action, data):
        if action["action"] == "search":
            return self._search(data)

        if action["action"] == "filter":
            return self._filter(data, action.get("threshold", 0))

        if action["action"] == "rank":
            return self._rank(data, action.get("boost"))

        return data

    def _search(self, data):
        return data

    def _filter(self, data, threshold):
        return [d for d in data if d.get("trust_score", 0) >= threshold]

    def _rank(self, data, boost):
        return sorted(data, key=lambda x: x.get("trust_score", 0), reverse=True)
