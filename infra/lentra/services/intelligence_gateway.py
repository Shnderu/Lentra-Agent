from lentra.core.execution.trace_context import TraceContext


class IntelligenceGateway:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def process(self, payload: dict):
        trace = TraceContext()

        trace.log("gateway_input", payload)

        result = self.orchestrator.analyze(payload, trace)

        trace.log("gateway_output", result)

        # attach trace for debugging
        if isinstance(result, dict):
            result["_trace"] = trace.dump()

        return result
