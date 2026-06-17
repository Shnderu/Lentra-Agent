import time


class AdaptiveTuner:

    def __init__(self, metrics_store):
        self.metrics = metrics_store

        # стартовые веса ranking
        self.weights = {
            "geo": 60,
            "budget": 40,
            "price": 20
        }

        # динамические thresholds
        self.latency_threshold = 1.5
        self.error_threshold = 3

        self.last_adjustment = time.time()

    # -------------------------
    # ADAPT THRESHOLDS
    # -------------------------

    def adjust_thresholds(self):

        snapshot = self.metrics.snapshot()

        avg_latency = sum(snapshot["latency_avg"].values()) / max(len(snapshot["latency_avg"]), 1)

        # если система стала медленнее → увеличиваем threshold
        if avg_latency > self.latency_threshold:
            self.latency_threshold *= 1.1

        # если система стабильна → ужесточаем
        else:
            self.latency_threshold *= 0.99

    # -------------------------
    # ADAPT RANKING WEIGHTS
    # -------------------------

    def adjust_weights(self):

        snapshot = self.metrics.snapshot()

        error_rate = sum(snapshot["errors"].values())

        # если много ошибок → уменьшаем агрессивность ranking
        if error_rate > self.error_threshold:
            self.weights["geo"] *= 0.95
            self.weights["budget"] *= 0.95
            self.weights["price"] *= 1.05

        else:
            # стабильная система → усиливаем персонализацию
            self.weights["geo"] *= 1.02
            self.weights["budget"] *= 1.01

    # -------------------------
    # MAIN LOOP
    # -------------------------

    def tick(self):

        now = time.time()

        # не чаще чем раз в 10 секунд
        if now - self.last_adjustment < 10:
            return

        self.adjust_thresholds()
        self.adjust_weights()

        self.last_adjustment = now

    def get_config(self):
        return {
            "latency_threshold": self.latency_threshold,
            "error_threshold": self.error_threshold,
            "weights": self.weights
        }
