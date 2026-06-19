from lentra.core.scenario.monetization_v1 import monetization_engine


class MultiScenarioRouterV1:

    def route(self, intent):
        """
        v1.1: return scenario set (not single scenario)
        """

        candidates = self._get_candidates(intent)

        scored = []

        for scenario in candidates:
            fake_intent = type("Intent", (), {
                "name": intent.name,
                "scenario": scenario,
                "payload": intent.payload
            })

            score = monetization_engine.score(fake_intent)

            scored.append((scenario, score.priority))

        # keep top 2 scenarios instead of 1
        top = sorted(scored, key=lambda x: x[1], reverse=True)[:2]

        intent.scenarios = [s[0] for s in top]

        return intent

    def _get_candidates(self, intent):

        if intent.name == "rent_search":
            return [
                "rent_scenario_v1",
                "pricing_scenario_v1"
            ]

        return ["default_scenario_v1"]
