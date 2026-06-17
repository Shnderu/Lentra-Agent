import time
from collections import defaultdict


class LatencyHistogram:
    def __init__(self):
        self.data = defaultdict(list)

    def observe(self, key: str, value: float):
        self.data[key].append(value)

    def summary(self, key: str):
        values = sorted(self.data.get(key, []))
        if not values:
            return None

        def pct(p):
            idx = int(len(values) * p)
            return values[min(idx, len(values) - 1)]

        return {
            "count": len(values),
            "p50": pct(0.5),
            "p95": pct(0.95),
            "p99": pct(0.99),
            "max": max(values),
        }


class EventGraph:
    def __init__(self):
        self.edges = []

    def link(self, parent, child):
        self.edges.append((parent, child))

    def dump(self):
        print("\n[EVENT GRAPH]")
        for p, c in self.edges:
            print(f"{p} -> {c}")
