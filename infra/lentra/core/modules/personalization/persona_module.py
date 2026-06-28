

class PersonaModule:

    def run(self, ctx):

        query = getattr(ctx, "query", "")

        # базовая эвристика (MVP уровень)
        persona = {
            "type": "expat_nomad",
            "budget_sensitivity": "high" if "cheap" in query else "medium",
            "priority": ["wifi", "location", "price"],
            "intent": "long_term_rent"
        }

        ctx.persona = persona

        return ctx
