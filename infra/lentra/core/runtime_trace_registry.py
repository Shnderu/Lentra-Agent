from typing import Dict, Any, List
from lentra.core.runtime_trace_v1 import RuntimeTraceV1


class TraceRegistry:
    """
    GLOBAL TRACE REGISTRY (v1)

    PURPOSE:
    - collect traces from runtime components
    - provide export API
    """

    def __init__(self):
        self.traces: Dict[str, RuntimeTraceV1] = {}

    def register(self, trace: RuntimeTraceV1):
        self.traces[trace.trace_id] = trace

    def export_all(self) -> Dict[str, Any]:
        return {
            "traces": {
                tid: trace.dump()
                for tid, trace in self.traces.items()
            }
        }

    def get(self, trace_id: str):
        return self.traces.get(trace_id)
