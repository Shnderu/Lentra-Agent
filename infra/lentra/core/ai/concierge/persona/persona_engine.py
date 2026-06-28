

class PersonaEngine:

    def profile(self, query: str):

        q = query.lower()

        persona = {
            "type": "unknown",
            "weights": {
                "price": 0.5,
                "location": 0.5,
                "internet": 0.5,
                "noise": 0.5,
                "comfort": 0.5
            }
        }

        # digital nomad detection
        if "wifi" in q or "internet" in q:
            persona["type"] = "digital_nomad"
            persona["weights"]["internet"] = 0.9
            persona["weights"]["noise"] = 0.7
            persona["weights"]["price"] = 0.5

        # budget seeker
        if "cheap" in q or "under" in q:
            persona["type"] = "budget_seeker"
            persona["weights"]["price"] = 0.9

        # beach lifestyle
        if "beach" in q:
            persona["weights"]["location"] = 0.8

        # expat logic
        if "long" in q or "month" in q:
            persona["type"] = "expat"
            persona["weights"]["comfort"] = 0.8

        return persona
