"""
RUNTIME TRACE AUDIT LAYER
Detects execution failures, silent fallbacks, and graph drift.
"""

import time
from typing import Any, Dict, List


class RuntimeTraceAudit:
    """
    Captures runtime execution truth of Intelligence Graph OS.
    """

    def __init__(self):
        self.traces: List[Dict[str, Any]] = []

    def start_trace(self, request_id: str):
        return {
            "request_id": request_id,
            "start_time": time.time(),
            "steps": [],
            "engines_called": [],
            "failures": [],
            "status": "running"
        }

    def log_step(self, trace: Dict, step_name: str, status: str):
        trace["steps"].append({
            "step": step_name,
            "status": status,
            "timestamp": time.time()
        })

    def log_engine(self, trace: Dict, engine: str, result: Any):
        trace["engines_called"].append({
            "engine": engine,
            "has_result": result is not None,
            "timestamp": time.time()
        })

    def log_failure(self, trace: Dict, error: str):
        trace["failures"].append({
            "error": error,
            "timestamp": time.time()
        })

    def finalize(self, trace: Dict):
        trace["end_time"] = time.time()
        trace["status"] = (
            "failed" if trace["failures"] else "success"
        )

        self.traces.append(trace)
        return trace

    def get_summary(self) -> Dict:
        total = len(self.traces)
        failed = len([t for t in self.traces if t["status"] == "failed"])

        return {
            "total_requests": total,
            "failed_requests": failed,
            "success_rate": (total - failed) / total if total else 0
        }
