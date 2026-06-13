# ============================================================
# OBSERVABILITY SERVICE V16.8
# ============================================================

import time
from lentra.observability.traces.model import RequestTrace
from lentra.observability.metrics.collector import MetricsCollector


class ObservabilityService:
    def __init__(self):
        self.metrics = MetricsCollector()

    def start_trace(self, request_id: str):
        return RequestTrace(request_id=request_id)

    def log_stage(self, trace: RequestTrace, stage: str, meta=None):
        trace.add(stage, meta)

    def record_cache_hit(self):
        self.metrics.record_cache_hit()

    def record_cache_miss(self):
        self.metrics.record_cache_miss()

    def record_request_start(self):
        self.metrics.record_request()

    def record_latency(self, start_time):
        self.metrics.record_latency(time.time() - start_time)

    def get_metrics(self):
        return self.metrics.snapshot()
