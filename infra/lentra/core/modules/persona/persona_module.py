
class PersonaModule:

    def run(self, ctx):

        # DEFAULT PERSONA (v2 safe mode)

        if not hasattr(ctx, "objects"):

            return ctx

        ctx.persona = {
            "type": "expat_nomad",
            "budget_sensitivity": "medium",
            "priority": ["wifi", "location", "price"],
            "intent": "long_term_rent"
        }

        return ctx
