class DecisionModule:
    def run(self, ctx):

        snapshot = ctx.snapshot
        objects = snapshot.objects

        for obj in objects:

            price = obj["price"]
            risk = obj["risk"]
            area = obj["area_score"]

            # SIMPLE stable scoring v3
            score = (area * 0.6) - (risk * 0.3)

            obj["final_score"] = round(score, 3)

            if score > 3.5:
                obj["verdict"] = "good"
            elif score > 2.5:
                obj["verdict"] = "neutral"
            else:
                obj["verdict"] = "bad"

        return ctx
