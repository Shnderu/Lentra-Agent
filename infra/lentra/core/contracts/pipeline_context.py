from dataclasses import dataclass, field, replace
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class PipelineContext:
    """
    Immutable context passed through all engines.
    NO in-place mutation allowed.
    """

    raw: Dict[str, Any]

    signals: Dict[str, Any] = field(default_factory=dict)
    dedup: Dict[str, Any] = field(default_factory=dict)
    coupling: Dict[str, Any] = field(default_factory=dict)
    risk: Dict[str, Any] = field(default_factory=dict)
    ranking: Dict[str, Any] = field(default_factory=dict)
    enrichment: Dict[str, Any] = field(default_factory=dict)

    def with_field(self, **changes) -> "PipelineContext":
        """
        SAFE immutable update (returns new instance)
        """
        return replace(self, **changes)

    def to_dict(self) -> Dict[str, Any]:
        """
        Final serialization layer (API-safe)
        """
        return {
            "pricing": self.raw.get("pricing"),
            "area": self.raw.get("area"),
            "dedup": self.dedup,
            "coupling": self.coupling,
            "risk": self.risk,
            "ranking": self.ranking,
            "enrichment": self.enrichment,
        }
