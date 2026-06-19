from dataclasses import dataclass


@dataclass
class ScenarioCost:
    name: str
    value_score: float   # бизнес-ценность
    cost_score: float    # стоимость исполнения
    priority: float      # итоговый вес


class MonetizationEngineV1:

    def score(self, intent):
        """
        Static scoring model (no ML, v1 freeze)
        """

        scenario = intent.scenario

        # -------------------------
        # FIXED SCORING TABLE
        # -------------------------

        if scenario == "rent_scenario_v1":
            return ScenarioCost(
                name=scenario,
                value_score=0.9,
                cost_score=0.2,
                priority=0.85
            )

        if scenario == "pricing_scenario_v1":
            return ScenarioCost(
                name=scenario,
                value_score=0.6,
                cost_score=0.1,
                priority=0.75
            )

        # fallback
        return ScenarioCost(
            name=scenario,
            value_score=0.3,
            cost_score=0.5,
            priority=0.4
        )


monetization_engine = MonetizationEngineV1()
