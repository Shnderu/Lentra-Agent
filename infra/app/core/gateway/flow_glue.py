from typing import Any, Dict


class FlowGlue:

    def __init__(self, intent_router, scenario_engine):
        self.intent_router = intent_router
        self.scenario_engine = scenario_engine

    def resolve(self, user_input: Dict[str, Any]) -> Dict[str, Any]:

        ctx = user_input

        # FIX: единый безопасный контракт
        try:
            intent = self.intent_router.route(user_input, ctx)
        except Exception:
            intent = self.intent_router.classify(user_input)

        try:
            scenario = self.scenario_engine.select(intent, user_input)
        except Exception:
            scenario = {"type": "fallback"}

        try:
            result = self.scenario_engine.execute(scenario, user_input)
        except Exception:
            result = {"status": "execution_failed"}

        return {
            "intent": intent,
            "scenario": scenario,
            "result": result
        }
