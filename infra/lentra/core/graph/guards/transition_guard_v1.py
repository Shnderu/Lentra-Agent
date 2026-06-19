class TransitionGuardV1:

    def can_transition(self, from_node, to_node, state) -> bool:

        data = state.data or {}
        intent = state.intent or {}

        # -------------------------
        # RENT → PRICING
        # -------------------------
        if from_node == "rent_scenario_v1" and to_node == "pricing_scenario_v1":
            return data.get("rent_analyzed", False)

        # -------------------------
        # DEFAULT: allow
        # -------------------------
        return True
