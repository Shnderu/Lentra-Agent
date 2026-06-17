import time


class SourceHealth:
    """
    Отслеживание состояния источников:
    - latency
    - failures
    - health score
    """

    def __init__(self):
        self.stats = {}

    def record_success(self, source: str, latency: float):
        s = self.stats.setdefault(source, {"ok": 0, "fail": 0, "lat": []})
        s["ok"] += 1
        s["lat"].append(latency)

    def record_fail(self, source: str):
        s = self.stats.setdefault(source, {"ok": 0, "fail": 0, "lat": []})
        s["fail"] += 1

    def health(self, source: str) -> float:
        s = self.stats.get(source)
        if not s:
            return 1.0

        total = s["ok"] + s["fail"]
        if total == 0:
            return 1.0

        success_rate = s["ok"] / total
        return round(success_rate, 2)

    def is_healthy(self, source: str) -> bool:
        return self.health(source) > 0.3

    def dump(self):
        print("\n[SOURCE HEALTH]")
        for k, v in self.stats.items():
            print(k, "health=", self.health(k), "raw=", v)
