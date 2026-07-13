from lentra.core.data_layer.pipeline.ingestion_pipeline import (
    IngestionPipeline
)

from lentra.core.data_layer.seeds.market_seed_v1 import (
    get_market_seed
)


class MarketSeedRunner:

    def __init__(self):
        self.pipeline = IngestionPipeline()


    def run(self):

        listings = get_market_seed()

        result = self.pipeline.ingest_batch(
            listings
        )

        return result


if __name__ == "__main__":

    runner = MarketSeedRunner()

    result = runner.run()

    print("=== MARKET SEED RESULT ===")

    print(
        {
            "ingested": result.get("ingested"),
            "clusters": result.get("clusters"),
            "enriched": result.get("enriched")
        }
    )

    print()

    for item in result.get("items", []):

        print(
            {
                "title": item.get("title"),
                "price_vnd": item.get("price_vnd"),
                "market_price": item.get("market_price"),
                "deviation": item.get("deviation_pct"),
                "risk": item.get("risk_level")
            }
        )
