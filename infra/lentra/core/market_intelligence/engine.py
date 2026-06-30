class MarketGraphEngine:

    def __init__(self,
        pricing,
        ranking,
        risk,
        dedup,
        geo,
        explanation,
        fusion
    ):
        self.pricing = pricing
        self.ranking = ranking
        self.risk = risk
        self.dedup = dedup
        self.geo = geo
        self.explanation = explanation
        self.fusion = fusion

    def execute(self, context: dict):

        listings = context.get("listings", [])

        listings = self.dedup.run(listings)

        pricing_data = self.pricing.run(listings)
        risk_data = self.risk.run(listings)
        geo_data = self.geo.run(listings)

        ranked = self.ranking.run(
            listings,
            pricing_data,
            risk_data,
            geo_data
        )

        fused = self.fusion.run(ranked)

        return self.explanation.run(fused)
