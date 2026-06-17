from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class APIResponse:
    trace_id: str
    query: str
    total: int
    returned: int
    items: List[Any]
    error: Optional[str] = None

    def to_dict(self):
        return {
            "trace_id": self.trace_id,
            "query": self.query,
            "total": self.total,
            "returned": self.returned,
            "items": self.items,
            "error": self.error
        }
