# ============================================================
# LENTRA METRICS COLLECTOR V16.8
# ============================================================

import time


class MetricsCollector:
    def __init__(self):
        self.data = {
            "requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_latency": 0,
        }

    def record_request(self):
        self.data["requests"] += 1

    def record_cache_hit(self):
        self.data["cache_hits"] += 1

    def record_cache_miss(self):
        self.data["cache_misses"] += 1

    def record_latency(self, value):
        self.data["total_latency"] += value

    def snapshot(self):
        req = self.data["requests"] or 1

        return {
            "requests": self.data["requests"],
            "cache_hit_rate": self.data["cache_hits"] / req,
            "avg_latency": self.data["total_latency"] / req,
        }
