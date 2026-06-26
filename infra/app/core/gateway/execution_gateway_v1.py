import traceback


class ExecutionGatewayV1:
    """
    Unified execution gateway:
    intent -> scenario -> execution pipeline
    """

    def __init__(self):
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
                from lentra.core.scenario.scenario_engine_v1 import ScenarioEngineV1
                self.scenario_engine = ScenarioEngineV1()
            except Exception:
                self.scenario_engine = None

    def execute(self, event: dict) -> dict:
        self._load_dependencies()

        try:
            if self.intent_router:
                intent = self.intent_router(event)
            else:
                intent = {"type": "fallback", "raw": event}

            # 🔥 FIX: НЕ ДАЁМ silent no_scenario_engine
            if self.scenario_engine:
                result = self.scenario_engine.run(intent)
            else:
                return {
                    "ok": False,
                    "error": "scenario_engine_not_available",
                    "intent": intent
                }

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
