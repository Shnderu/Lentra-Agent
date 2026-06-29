import time
from collections import defaultdict
import math


class TemporalMarketEngine:
    """
    Time-aware market memory.

    Adds:
    - decay weighting
    - volatility tracking
    - robust baseline
    """

    def __init__(self):
        # cluster -> list of (price, timestamp)
        self.data = defaultdict(list)

        self.decay_half_life = 7 * 24 * 3600  # 7 days

    # -------------------------
    # TIME DECAY WEIGHT
    # -------------------------
    def _weight(self, ts: float) -> float:
        age = time.time() - ts
        return math.exp(-age / self.decay_half_life)

    # -------------------------
    # INGEST
    # -------------------------
    def update(self, key: str, price: float):
        self.data[key].append((float(price), time.time()))

    # -------------------------
    # WEIGHTED MEDIAN
    # -------------------------
    def weighted_median(self, key: str) -> float:
        values = self.data.get(key, [])

        if len(values) < 3:
            return 500.0

        weighted = []

        for price, ts in values:
            w = self._weight(ts)
            weighted.append((price, w))

        weighted.sort(key=lambda x: x[0])

        total = sum(w for _, w in weighted)
        acc = 0

        for price, w in weighted:
            acc += w
            if acc >= total / 2:
                return price

        return weighted[-1][0]

    # -------------------------
    # VOLATILITY
    # -------------------------
    def volatility(self, key: str) -> float:
        values = self.data.get(key, [])

        if len(values) < 3:
            return 0.5

        prices = [p for p, _ in values[-20:]]

        mean = sum(prices) / len(prices)
        var = sum((p - mean) ** 2 for p in prices) / len(prices)

        return min(1.0, math.sqrt(var) / (mean + 1e-6))

    # -------------------------
    # DEVIATION
    # -------------------------
    def deviation(self, key: str, price: float) -> float:
        baseline = self.weighted_median(key)

        if baseline <= 0:
            return 0.0

        return (price - baseline) / baseline
