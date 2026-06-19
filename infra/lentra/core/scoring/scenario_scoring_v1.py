class ScenarioScoringV1:

    def score(self, intent, scenario_name) -> float:

        name = intent.get("name")

        # -------------------------
        # RENT SCORING
        # -------------------------
        if scenario_name == "rent_scenario_v1":
            if name == "rent_search":
                return 1.0
            return 0.2

        # -------------------------
        # PRICING SCORING
        # -------------------------
        if scenario_name == "pricing_scenario_v1":
            if intent.get("payload", {}).get("text"):
                text = intent["payload"]["text"]
                if any(k in text.lower() for k in ["price", "cost", "rent"]):
                    return 0.8
            return 0.1

        # DEFAULT
        return 0.05
