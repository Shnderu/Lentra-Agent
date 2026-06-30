class IntelligencePipelineOrchestrator:

    def __init__(self, engine=None):
        self.engine = engine

    def execute(self, request):
        if not self.engine:
            raise RuntimeError("Engine not injected (bootstrap violation)")

        return self.engine.run(request)
