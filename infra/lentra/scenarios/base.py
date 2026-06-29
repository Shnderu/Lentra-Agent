from typing import Dict, Any, Protocol


class Scenario(Protocol):
    name: str

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        ...
