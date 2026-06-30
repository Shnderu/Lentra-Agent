from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ExecutionContext:
    request_id: str
    query_text: str
    metadata: Dict[str, Any]

    def child(self, **kwargs) -> "ExecutionContext":
        data = {
            "request_id": self.request_id,
            "query_text": self.query_text,
            "metadata": dict(self.metadata),
        }
        data.update(kwargs)
        return ExecutionContext(**data)
