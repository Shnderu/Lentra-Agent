from dataclasses import dataclass, field
from typing import Any, Dict, List
import time


@dataclass
class TraceEvent:
    node: str
    timestamp: float
    input_state: Dict[str, Any]
    output_state: Dict[str, Any]


@dataclass
class ExecutionTraceV1:
    events: List[TraceEvent] = field(default_factory=list)

    def record(self, node: str, input_state: Dict[str, Any], output_state: Dict[str, Any]):
        self.events.append(
            TraceEvent(
                node=node,
                timestamp=time.time(),
                input_state=input_state,
                output_state=output_state or {}
            )
        )

    def export(self):
        return [
            {
                "node": e.node,
                "ts": e.timestamp,
                "input": e.input_state,
                "output": e.output_state
            }
            for e in self.events
        ]
