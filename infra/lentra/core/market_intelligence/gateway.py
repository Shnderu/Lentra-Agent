class IntelligenceGateway:
    """
    SAFE GATEWAY LAYER

    CRITICAL RULE:
    - NO orchestrator creation inside gateway
    - orchestrator MUST be injected
    """

    def __init__(self, orchestrator=None):
        # FIX: do not construct Orchestrator internally (break recursion)
        self.orchestrator = orchestrator

    def execute(self, context):
        if not self.orchestrator:
            raise RuntimeError("Orchestrator not injected into gateway")

        return self.orchestrator.run(context)
