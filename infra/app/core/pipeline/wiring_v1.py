from app.core.intent.intent_router_v1 import build_query
from app.core.scenario.scenario_engine_v1 import run_scenario
from app.core.adapters.rent_data_adapter_v1 import RentDataAdapterV1


# =========================
# RANKING (v1 MONETIZATION LOGIC)
# =========================

def rank_listings(listings):
    if not listings:
        return []

    def score(item):
        base = 0

        # premium boost (монетизация будущая)
        if item.get("source") == "premium":
            base += 100

        # price heuristic (чем более "валидная" цена — тем выше)
        price = item.get("price")
        if isinstance(price, (int, float)):
            if 500 <= price <= 2000:
                base += 50
            elif 2000 < price <= 4000:
                base += 30
            else:
                base += 10

        # city match boost (если появится фильтр позже)
        if item.get("city"):
            base += 5

        return base

    return sorted(listings, key=score, reverse=True)


# =========================
# CORE PIPELINE ADAPTER
# =========================

async def execute_pipeline(query):
    """
    Domain execution layer v1:
    real data + ranking + monetization hooks
    """

    adapter = RentDataAdapterV1()

    listings = await adapter.get_rent_listings(query)
    ranked = rank_listings(listings)

    class Context:
        def __init__(self, query, listings, ranked):
            self.query = query
            self.listings = listings
            self.ranked = ranked
            self.insights = {}

    return Context(query, listings, ranked)


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
