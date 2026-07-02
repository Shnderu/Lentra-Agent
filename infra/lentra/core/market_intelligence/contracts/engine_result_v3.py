from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class EngineResultV3:
    status: str
    data: Dict[str, Any]

    def as_dict(self):
        return {
            "status": self.status,
            **self.data
        }
