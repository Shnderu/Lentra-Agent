from dataclasses import dataclass, asdict
from typing import Any, Dict, List
import time


@dataclass
class EngineTrace:
    name: str
    duration_ms: float
    input_size: int
    output_size: int


@dataclass
class RequestTrace:
    query: str
    start_time: float
    end_time: float
    engines: List[EngineTrace]
    final_score: float


class TraceCollector:
    """
    Lightweight observability layer (no external deps)
    """

    def __init__(self):
        self._engines: List[EngineTrace] = []
        self._start_time = None
        self._query = None

    def start(self, query: str):
        self._query = query
        self._start_time = time.time()
        self._engines = []

    def record_engine(
        self,
        name: str,
        duration_ms: float,
        input_data: Any,
        output_data: Any
    ):
        self._engines.append(
            EngineTrace(
                name=name,
                duration_ms=round(duration_ms, 3),
                input_size=len(str(input_data)),
                output_size=len(str(output_data))
            )
        )

    def finish(self, final_score: float) -> Dict[str, Any]:
        end_time = time.time()

        trace = RequestTrace(
            query=self._query,
            start_time=self._start_time,
            end_time=end_time,
            engines=self._engines,
            final_score=final_score
        )

        return {
            "trace": {
                "query": trace.query,
                "duration_ms": round((end_time - self._start_time) * 1000, 3),
                "final_score": final_score,
                "engines": [asdict(e) for e in trace.engines]
            }
        }
