class RankingEngine:
    """
    Ranks market objects into final ordering score
    """

    def run(self, ctx):

        objects = getattr(ctx.snapshot, "objects", [])

        def score(o):
            price_score = 1.0 / (1.0 + abs(getattr(o, "market_price", 0) - ctx.snapshot.average_market_price))
            risk_penalty = getattr(o, "risk", 0.5)
            area = getattr(o, "area_score", 5.0)

            return (price_score * 0.5) + (area * 0.3) - (risk_penalty * 0.2)

        for obj in objects:
            obj.final_score = score(obj)

        ctx.snapshot.objects = sorted(objects, key=lambda x: x.final_score, reverse=True)

        return ctx
