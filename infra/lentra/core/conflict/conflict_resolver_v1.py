class ConflictResolverV1:

    def resolve(self, scored_scenarios):

        """
        scored_scenarios = [
            {"name": "rent_scenario_v1", "score": 0.9},
            {"name": "pricing_scenario_v1", "score": 0.8}
        ]
        """

        # сортировка по score
        sorted_scenarios = sorted(
            scored_scenarios,
            key=lambda x: x["score"],
            reverse=True
        )

        primary = sorted_scenarios[0] if sorted_scenarios else None

        secondary = [
            s for s in sorted_scenarios[1:]
            if s["score"] > 0.3
        ]

        return {
            "primary": primary,
            "secondary": secondary
        }
