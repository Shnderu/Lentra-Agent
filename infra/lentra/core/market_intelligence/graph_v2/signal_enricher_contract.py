from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class EnrichmentResult:
    query: str
    nodes: List[str]
    symbols: List[str]
    files: List[str]
    intent: str | None = None
    metadata: Dict[str, Any] | None = None
