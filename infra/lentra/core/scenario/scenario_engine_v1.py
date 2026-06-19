class ScenarioEngineV1:

    def execute_node(self, node, state):

        enriched = {
            "node": node,
            "processed_intent": state.intent.get("name"),
            "payload": state.intent.get("payload"),
        }

        # -------------------------
        # RENT FLOW
        # -------------------------
        if node == "rent_scenario_v1":

            state.data["rent_analyzed"] = True

            # FIX: stop implicit cascade unless condition met
            if state.intent.get("name") != "rent_search":
                return {"data": enriched}

            return {
                "data": enriched,
                "next": ["pricing_scenario_v1"]  # explicit routing
            }

        # -------------------------
        # PRICING FLOW
        # -------------------------
        if node == "pricing_scenario_v1":

            # only run if explicitly triggered OR routed
            if not state.data.get("rent_analyzed"):
                return {"data": enriched}

            state.data["pricing_checked"] = True

            return {"data": enriched}

        return {"data": enriched}

    def execute(self, node, state):
        return self.execute_node(node, state)


scenario_engine = ScenarioEngineV1()
