from typing import Dict, Any
from lentra.core.observability.trace_collector import TraceCollector


class ObservabilityGatewayWrapper:
    def __init__(self, gateway):
        self.gateway = gateway
        self.trace = TraceCollector()

    def handle(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        trace_id = self.trace.start(payload)

        self.trace.event(trace_id, "gateway_start")

        result = self.gateway.handle(payload)

        self.trace.event(trace_id, "gateway_end")

        self.trace.finish(trace_id, result)

        result["_trace_id"] = trace_id
        return result
