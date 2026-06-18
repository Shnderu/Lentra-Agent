from app.core.intent.intent_router_v1 import build_query
from app.core.scenario.scenario_engine_v1 import run_scenario


# =========================
# CORE PIPELINE ADAPTER (stub boundary)
# =========================

async def execute_pipeline(query):
    """
    Единая точка входа в domain core v1.
    Сейчас — stub.
    Позже будет подключён:
    - real estate adapters
    - ranking engine
    - normalizers
    """
    class Context:
        def __init__(self, query):
            self.query = query
            self.ranked = []
            self.insights = {}

    return Context(query)


# =========================
# MAIN ENTRY (INTENT → SCENARIO → CORE)
# =========================

async def execute(text: str, meta: dict | None = None, **kwargs):
    query = build_query(text, meta)

    result = await run_scenario(
        intent=query.intent,
        query=query,
        pipeline_fn=execute_pipeline,
        **kwargs
    )

    return result
