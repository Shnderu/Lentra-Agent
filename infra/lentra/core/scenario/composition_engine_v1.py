from dataclasses import dataclass
from typing import List


@dataclass
class ExecutionStep:
    scenario: str
    weight: float


class CompositionEngineV1:

    def build(self, intent, scenarios):
        """
        Convert multiple scenarios into execution plan
        """

        steps: List[ExecutionStep] = []

        for s in scenarios:
            # static weighting rule v1
            if s == "rent_scenario_v1":
                steps.append(ExecutionStep(s, 0.7))

            elif s == "pricing_scenario_v1":
                steps.append(ExecutionStep(s, 0.3))

            else:
                steps.append(ExecutionStep(s, 0.1))

        # sort by weight (execution order)
        steps = sorted(steps, key=lambda x: x.weight, reverse=True)

        return steps


composition_engine = CompositionEngineV1()
