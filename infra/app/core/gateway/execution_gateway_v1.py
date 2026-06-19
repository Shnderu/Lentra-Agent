import traceback

# Core execution boundary (FROZEN v1)
# This module becomes the ONLY allowed entrypoint for runtime flows:
# API / BOT / WORKER must eventually converge here.

class ExecutionGatewayV1:
    """
    Unified execution gateway:
    intent -> scenario -> execution pipeline
    """

    def __init__(self):
        # lazy imports to avoid circular dependency issues
        self.intent_router = None
        self.scenario_engine = None

    def _load_dependencies(self):
        if self.intent_router is None:
            try:
                from lentra.intent.router import route as intent_route
                self.intent_router = intent_route
            except Exception:
                try:
                    from app.intent.router import route as intent_route
                    self.intent_router = intent_route
                except Exception:
                    self.intent_router = None

        if self.scenario_engine is None:
            try:
                from app.core.scenario.scenario_engine_v1 import ScenarioEngineV1
                self.scenario_engine = ScenarioEngineV1()
            except Exception:
                self.scenario_engine = None

    def execute(self, event: dict) -> dict:
        """
        Main execution contract.
        Input: normalized event (api/bot/worker)
        Output: unified response
        """

        self._load_dependencies()

        try:
            # 1. INTENT PHASE
            if self.intent_router:
                intent = self.intent_router(event)
            else:
                intent = {"type": "fallback", "raw": event}

            # 2. SCENARIO PHASE
            if self.scenario_engine:
                result = self.scenario_engine.run(intent)
            else:
                result = {
                    "status": "no_scenario_engine",
                    "intent": intent
                }

            # 3. RESPONSE WRAP
            return {
                "ok": True,
                "intent": intent,
                "result": result
            }

        except Exception as e:
            traceback.print_exc()
            return {
                "ok": False,
                "error": str(e),
                "intent": None,
                "result": None
            }


# singleton (simple freeze model)
gateway = ExecutionGatewayV1()


def execute(event: dict) -> dict:
    return gateway.execute(event)
