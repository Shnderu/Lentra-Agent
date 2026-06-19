from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class ExecutionStateV1:
    intent: Dict[str, Any]
    data: Dict[str, Any] = field(default_factory=dict)
    trace: List[str] = field(default_factory=list)

    def add_trace(self, node: str):
        self.trace.append(node)

    def merge(self, payload: Dict[str, Any]):
        if not payload:
            return

        if "data" in payload and isinstance(payload["data"], dict):
            self.data.update(payload["data"])
