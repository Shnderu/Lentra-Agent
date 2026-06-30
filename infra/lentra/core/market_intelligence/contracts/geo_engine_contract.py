from typing import Protocol, Dict, Any, runtime_checkable


@runtime_checkable
class GeoEngineContract(Protocol):
    """
    Geo Layer Contract:
    enrich listing with location intelligence
    """

    def analyze(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        ...
