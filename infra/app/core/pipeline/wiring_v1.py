from lentra.core.intent.intent_router_v1 import build_query
from lentra.core.scenario.scenario_engine_v1 import run_scenario
from lentra.core.adapters.rent_data_adapter_v1 import RentDataAdapterV1
from lentra.core.pipeline.response_formatter_v1 import format_response


# =========================
# RANKING v1
# =========================

def rank_listings(listings):
    if not listings:
        return []

    def score(item):
        base = 0

        if item.get("source") == "premium":
            base += 100

        price = item.get("price")
        if isinstance(price, (int, float)):
            if 500 <= price <= 2000:
                base += 50
            elif 2000 < price <= 4000:
                base += 30
            else:
                base += 10

        if item.get("city"):
            base += 5

        return base

    return sorted(listings, key=score, reverse=True)


# =========================
# PIPELINE
# =========================

async def execute_pipeline(query):
    adapter = RentDataAdapterV1()

    listings = await adapter.get_rent_listings(query)
    ranked = rank_listings(listings)

    class Context:
        def __init__(self):
            self.query = query
            self.listings = listings
            self.ranked = ranked

    return Context()


# =========================
# ENTRY POINT
# =========================

async def execute(text: str, meta: dict | None = None, **kwargs):
    query = build_query(text, meta)

    result = await run_scenario(
        intent=query.intent,
        query=query,
        pipeline_fn=execute_pipeline,
        **kwargs
    )

    return format_response(result)
