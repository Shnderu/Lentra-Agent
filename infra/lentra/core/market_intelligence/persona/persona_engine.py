class PersonaEngine:
    """
    Adjusts ranking based on user intent (future layer)
    """

    def run(self, ctx):
        # пока stub (v3)
        ctx.persona = {
            "mode": "default",
            "bias": 1.0
        }
        return ctx
