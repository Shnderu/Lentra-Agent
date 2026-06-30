from lentra.core.market_intelligence.pipeline.intelligence_pipeline_orchestrator import IntelligencePipelineOrchestrator


class IntelligenceOrchestrator:
    def __init__(self):
        self.pipeline = IntelligencePipelineOrchestrator(self)

    def analyze(self, intent, trace=None):
        if trace:
            trace.log("orchestrator_input", intent)

        listings = intent.get("listings", [])
        query_text = intent.get("query_text", "")

        result = self.pipeline.run(listings, query_text, trace)

        if trace:
            trace.log("orchestrator_output", result)

        return result
