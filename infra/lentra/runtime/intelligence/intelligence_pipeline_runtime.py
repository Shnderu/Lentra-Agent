from lentra.core.market_intelligence.pipeline.intelligence_pipeline_orchestrator import IntelligencePipelineOrchestrator
from lentra.runtime.observability.runtime_trace_audit import RuntimeTraceAudit

class PipelineRuntime:

    def __init__(self):
        self.core = IntelligencePipelineOrchestrator()
        self.audit = RuntimeTraceAudit()

    def run(self, data):
        self.audit.trace("pipeline_start", data)
        result = self.core.run(data)
        self.audit.trace("pipeline_end", result)
        return result
