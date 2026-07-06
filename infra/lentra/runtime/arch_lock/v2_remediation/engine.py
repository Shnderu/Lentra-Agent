from dataclasses import dataclass
from typing import List

@dataclass
class RemediationAction:
    type: str
    target: str
    patch: str | None = None


class RemediationEngine:
    def __init__(self):
        self.actions: List[RemediationAction] = []

    def plan(self, violations: list) -> List[RemediationAction]:
        actions = []

        for v in violations:
            if "NO_RUNTIME_TO_CORE" in str(v):
                actions.append(RemediationAction(
                    type="REWIRE_DEPENDENCY",
                    target=str(v),
                    patch=None
                ))

        return actions

    def apply(self, actions: List[RemediationAction]):
        return {"applied": len(actions)}
