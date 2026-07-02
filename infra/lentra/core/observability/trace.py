from dataclasses import dataclass, field
from time import time
from typing import Dict, Any, List, Optional
import uuid


@dataclass
class EngineSpan:
    name: str
    start: float
    end: Optional[float] = None
    error: Optional[str] = None

    def finish(self):
        self.end = time()

    def latency_ms(self) -> float:
        if not self.end:
            return 0.0
        return round((self.end - self.start) * 1000, 3)


@dataclass
class RequestTrace:
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start: float = field(default_factory=time)
    spans: List[EngineSpan] = field(default_factory=list)

    def start_engine(self, name: str) -> EngineSpan:
        span = EngineSpan(name=name, start=time())
        self.spans.append(span)
        return span

    def snapshot(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "total_ms": round((time() - self.start) * 1000, 3),
            "engines": [
                {
                    "name": s.name,
                    "latency_ms": s.latency_ms(),
                    "error": s.error
                }
                for s in self.spans
            ]
        }
