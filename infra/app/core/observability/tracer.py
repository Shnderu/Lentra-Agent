import time
from app.core.observability.metrics_store import MetricsStore
from app.core.observability.anomaly_detector import AnomalyDetector
from app.core.adaptive.tuner import AdaptiveTuner


class Tracer:

    def __init__(self):
        self.metrics = MetricsStore()
        self.spans = {}
        self.detector = AnomalyDetector(self.metrics)
        self.tuner = AdaptiveTuner(self.metrics)

    def start(self, trace_id: str, stage: str):
        self.spans[(trace_id, stage)] = time.time()

    def end(self, trace_id: str, stage: str):
        key = (trace_id, stage)

        if key not in self.spans:
            return

        start = self.spans.pop(key)
        duration = time.time() - start

        self.metrics.record_latency(stage, duration)

        # 🔥 anomaly detection
        self.detector.analyze()

        # 🔥 adaptive tuning
        self.tuner.tick()

    def get_metrics(self):
        return self.metrics.snapshot()

    def get_alerts(self):
        return self.detector.alerts.get_alerts()

    def get_tuning(self):
        return self.tuner.get_config()
