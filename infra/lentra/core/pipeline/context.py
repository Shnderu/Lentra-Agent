from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class PipelineContext:
    """
    Immutable state container for all pipeline stages.
    NO MUTATION ALLOWED.
    """

    raw: Dict[str, Any]

    pricing: Dict[str, Any] = field(default_factory=dict)
    area: Dict[str, Any] = field(default_factory=dict)
    dedup: Dict[str, Any] = field(default_factory=dict)

    coupling: Dict[str, Any] = field(default_factory=dict)
    risk: Dict[str, Any] = field(default_factory=dict)
    ranking: Dict[str, Any] = field(default_factory=dict)

    enrichment: Dict[str, Any] = field(default_factory=dict)

    def with_update(self, **kwargs):
        """
        Functional update: returns new immutable instance
        """
        data = self.__dict__.copy()
        data.update(kwargs)
        return PipelineContext(**data)
