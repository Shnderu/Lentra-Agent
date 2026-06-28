from dataclasses import dataclass


class ConfidenceEngine:
    """
    Calculates confidence score for market objects
    """

    def run(self, ctx):
        objects = getattr(ctx.snapshot, "objects", [])

        for obj in objects:
            # базовая уверенность: риск обратно влияет
            base = 1.0 - float(getattr(obj, "risk", 0.5))
            obj.confidence = max(0.0, min(1.0, base))

        return ctx
