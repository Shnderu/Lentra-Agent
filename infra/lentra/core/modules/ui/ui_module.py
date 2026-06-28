from lentra.core.contracts.pipeline_context import PipelineContext


class UIModule:

    def run(self, ctx: PipelineContext) -> PipelineContext:

        objects = []

        for obj in ctx.snapshot.objects:

            if hasattr(obj, "to_ui_payload"):
                objects.append(obj.to_ui_payload())
            else:
                objects.append({
                    "id": getattr(obj, "id", None),
                    "price": getattr(obj, "market_price", None),
                    "risk": getattr(obj, "risk", None),
                    "area_score": getattr(obj, "area_score", None),
                    "verdict": getattr(obj, "verdict", None)
                })

        ctx.ui = {
            "query": ctx.snapshot.query,
            "total": ctx.snapshot.total_objects,
            "average_price": ctx.snapshot.average_market_price,
            "objects": objects
        }

        return ctx
