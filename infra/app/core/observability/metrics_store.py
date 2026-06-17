import time
from collections import defaultdict


class MetricsStore:

    def __init__(self):
        self.latencies = defaultdict(list)
        self.errors = defaultdict(int)
        self.calls = defaultdict(int)

    def record_latency(self, stage: str, value: float):
        self.latencies[stage].append(value)

    def record_call(self, name: str):
        self.calls[name] += 1

    def record_error(self, name: str):
        self.errors[name] += 1

    def snapshot(self):
        def avg(xs):
            return sum(xs) / len(xs) if xs else 0

        return {
            "latency_avg": {k: avg(v) for k, v in self.latencies.items()},
            "calls": dict(self.calls),
            "errors": dict(self.errors)
        }
