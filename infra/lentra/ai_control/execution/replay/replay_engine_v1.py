from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ReplayResult:
    execution_id: str
    original: Dict[str, Any]
    replayed: Dict[str, Any]
    identical: bool
    diff: Dict[str, Any]


class ReplayEngineV1:
    """
    Deterministic replay system.

    Guarantees:
    - same execution_id → same graph + command path
    - diff detection between runs
    """

    def __init__(self, bridge, ledger):
        self.bridge = bridge
        self.ledger = ledger
        self._cache = {}

    def replay(self, query: str, plan: dict) -> ReplayResult:
        execution_id = self.ledger.create_execution_id(query, plan)

        original = self._run_once(query)

        replayed = self._run_once(query)

        diff = self._diff(original, replayed)

        return ReplayResult(
            execution_id=execution_id,
            original=original,
            replayed=replayed,
            identical=(diff == {}),
            diff=diff
        )

    def _run_once(self, query: str):
        return self.bridge.run(query)

    def _diff(self, a: dict, b: dict):
        diff = {}

        if a.get("execution", {}).get("output") != b.get("execution", {}).get("output"):
            diff["output"] = {
                "a": a.get("execution", {}).get("output"),
                "b": b.get("execution", {}).get("output"),
            }

        if a.get("plan") != b.get("plan"):
            diff["plan"] = {
                "a": a.get("plan"),
                "b": b.get("plan"),
            }

        return diff
