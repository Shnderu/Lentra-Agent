class ScenarioPolicyV1:

    def should_run_node(self, node, state) -> bool:

        intent = state.intent.get("name")

        # -------------------------
        # RENT POLICY
        # -------------------------
        if node == "rent_scenario_v1":

            # только rent_search активирует сценарий
            return intent == "rent_search"

        # -------------------------
        # PRICING POLICY
        # -------------------------
        if node == "pricing_scenario_v1":

            # pricing только после анализа аренды
            return state.data.get("rent_analyzed", False)

        return True
