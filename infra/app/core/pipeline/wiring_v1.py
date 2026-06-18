from app.core.intent.intent_router_v1 import build_query
from app.core.scenario.scenario_engine_v1 import run_scenario
from app.core.adapters.rent_data_adapter_v1 import RentDataAdapterV1


# =========================
# CORE PIPELINE ADAPTER
# =========================

async def execute_pipeline(query):
    """
    Domain execution layer v1:
    теперь подключены реальные данные
    """

    adapter = RentDataAdapterV1()

    listings = await adapter.get_rent_listings(query)

    class Context:
        def __init__(self, query, listings):
            self.query = query
            self.listings = listings
            self.ranked = []
            self.insights = {}

    return Context(query, listings)


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
