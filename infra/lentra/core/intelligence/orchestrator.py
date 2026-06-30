from lentra.core.market_intelligence.pipeline.intelligence_pipeline_orchestrator import IntelligencePipelineOrchestrator

class Orchestrator:
    """
    SINGLE SOURCE OF TRUTH ORCHESTRATOR

    FIX:
    - no auto pipeline creation in other layers
    - single ownership of pipeline lifecycle
    """

    def __init__(self):
        self.pipeline = IntelligencePipelineOrchestrator()

    def run(self, context):
        return self.pipeline.execute(context)

from lentra.core.execution.trace_layer import TraceLayer

_trace = TraceLayer()
_trace.emit("orchestrator.init")

