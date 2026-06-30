from typing import Protocol, List, Dict, Any, runtime_checkable


@runtime_checkable
class DedupEngineContract(Protocol):
    """
    Stable AI OS contract:
    Dedup layer must always expose analyze(listings) -> deduped_listings
    """

    def analyze(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ...
