# ============================================================
# LENTRA OBSERVABILITY SERVICE V17.1 (FIXED IMPORT CYCLE)
# ============================================================

import time
from typing import Dict, Any, Optional

from lentra.observability.traces.model import RequestTrace
from lentra.observability.metrics.collector import MetricsCollector


class ObservabilityService:
    def __init__(self):
        self.metrics = MetricsCollector()
        self.traces: Dict[str, RequestTrace] = {}
        self._last_system_check = 0

    # ============================================================
    # TRACE API
    # ============================================================

    def start_trace(self, request_id: str) -> RequestTrace:
        trace = RequestTrace(request_id=request_id)
        self.traces[request_id] = trace
        return trace

    def log_stage(self, trace: RequestTrace, stage: str, meta=None):
        trace.add(stage, meta)

    def get_trace(self, request_id: str) -> Optional[Dict[str, Any]]:
        trace = self.traces.get(request_id)
        if not trace:
            return None

        return {
            "request_id": trace.request_id,
            "events": [
                {
                    "stage": e.stage,
                    "timestamp": e.timestamp,
                    "meta": e.meta
                }
                for e in trace.events
            ]
        }

    # ============================================================
    # METRICS
    # ============================================================

    def record_cache_hit(self):
        self.metrics.record_cache_hit()

    def record_cache_miss(self):
        self.metrics.record_cache_miss()

    def record_request_start(self):
        self.metrics.record_request()

    def record_latency(self, start_time: float):
        self.metrics.record_latency(time.time() - start_time)

    def get_metrics(self) -> Dict[str, Any]:
        return self.metrics.snapshot()

    # ============================================================
    # SYSTEM SNAPSHOT
    # ============================================================

    def get_system_snapshot(self) -> Dict[str, Any]:
        self._last_system_check = time.time()

        return {
            "timestamp": self._last_system_check,
            "metrics": self.get_metrics(),
            "observability_traces": len(self.traces),
            "status": "ok"
        }

    # ============================================================
    # QUEUE SNAPSHOT (NO DEPENDENCY ON CONSUMER)
    # ============================================================

    def get_queue_snapshot(self, conn=None) -> Dict[str, Any]:
        if conn is None:
            return {
                "status": "no_connection",
                "pending": None,
                "processing": None,
                "delivered": None
            }

        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT status, COUNT(*)
                FROM processing_queue
                GROUP BY status
            """)

            rows = cur.fetchall()

            result = {r[0]: r[1] for r in rows}

            return {
                "status": "ok",
                "pending": result.get("pending", 0),
                "processing": result.get("processing", 0),
                "delivered": result.get("delivered", 0),
                "failed": result.get("failed", 0)
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    # ============================================================
    # DEBUG DUMP
    # ============================================================

    def debug_dump(self, request_id: Optional[str] = None) -> Dict[str, Any]:
        return {
            "system": self.get_system_snapshot(),
            "trace": self.get_trace(request_id) if request_id else None,
            "metrics": self.get_metrics()
        }
