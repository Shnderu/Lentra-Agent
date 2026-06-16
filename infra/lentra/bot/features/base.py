from typing import Protocol, Dict, Any


class FeatureHandler(Protocol):
    async def __call__(self, ctx: Dict[str, Any]) -> str:
        ...
