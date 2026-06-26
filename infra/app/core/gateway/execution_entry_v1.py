from app.core.gateway.flow_glue import FlowGlue


class ExecutionEntryV1:
    """
    Single canonical entrypoint for ALL runtime flows.

    API / BOT / WORKER MUST eventually call only this.
    """

    def __init__(self, intent_router, scenario_engine):
        self.glue = FlowGlue(intent_router, scenario_engine)

    def handle(self, payload: dict) -> dict:
        if not isinstance(payload, dict):
            return {"ok": False, "error": "invalid_payload_type"}

        return self.glue.resolve(payload)


# =========================
# SINGLETON STATE
# =========================

entrypoint = None


def init(intent_router, scenario_engine):
    """
    HARD FIX:
    гарантированная инициализация entrypoint
    """
    global entrypoint
    entrypoint = ExecutionEntryV1(intent_router, scenario_engine)


def execute(payload: dict) -> dict:
    """
    SAFE EXECUTION LAYER:
    если не инициализирован — пробуем lazy init
    """

    global entrypoint

    if entrypoint is None:
        try:
            # lazy import fallback (минимальный safe bootstrap)
            from lentra.core.scenario.scenario_engine_v1 import ScenarioEngineV1
            from lentra.bot.core.intent_router import IntentRouter
        except Exception:
            return {
                "ok": False,
                "error": "execution_entry_not_initialized"
            }

        try:
            intent_router = IntentRouter()
            scenario_engine = ScenarioEngineV1()
            init(intent_router, scenario_engine)
        except Exception:
            return {
                "ok": False,
                "error": "execution_entry_init_failed"
            }

    return entrypoint.handle(payload)
