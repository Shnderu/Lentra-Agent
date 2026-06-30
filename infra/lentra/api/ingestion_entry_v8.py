from lentra.core.market_intelligence.ingestion.ingestion_router_v8 import IngestionRouterV8

router = IngestionRouterV8()


def process_market_feed(payload: dict):

    listings = payload.get("listings", [])

    return router.process(listings)
