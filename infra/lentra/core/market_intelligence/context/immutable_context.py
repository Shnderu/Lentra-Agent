from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class ImmutableContext:
    """
    STEP 1.1 - Frozen Context Layer

    RULES:
    - NO mutation allowed
    - NO engine logic inside
    - ONLY snapshot container
    - safe to pass through all engines
    """

    payload: Dict[str, Any]
    signals: Dict[str, Any] = field(default_factory=dict)

    coupling: Dict[str, Any] = field(default_factory=dict)
    risk: Dict[str, Any] = field(default_factory=dict)
    ranking: Dict[str, Any] = field(default_factory=dict)

    meta: Dict[str, Any] = field(default_factory=dict)

    def with_signals(self, signals: Dict[str, Any]) -> "ImmutableContext":
        return ImmutableContext(
            payload=self.payload,
            signals=signals,
            coupling=self.coupling,
            risk=self.risk,
            ranking=self.ranking,
            meta=self.meta,
        )

    def with_coupling(self, coupling: Dict[str, Any]) -> "ImmutableContext":
        return ImmutableContext(
            payload=self.payload,
            signals=self.signals,
            coupling=coupling,
            risk=self.risk,
            ranking=self.ranking,
            meta=self.meta,
        )

    def with_risk(self, risk: Dict[str, Any]) -> "ImmutableContext":
        return ImmutableContext(
            payload=self.payload,
            signals=self.signals,
            coupling=self.coupling,
            risk=risk,
            ranking=self.ranking,
            meta=self.meta,
        )

    def with_ranking(self, ranking: Dict[str, Any]) -> "ImmutableContext":
        return ImmutableContext(
            payload=self.payload,
            signals=self.signals,
            coupling=self.coupling,
            risk=self.risk,
            ranking=ranking,
            meta=self.meta,
        )

    def with_meta(self, meta: Dict[str, Any]) -> "ImmutableContext":
        return ImmutableContext(
            payload=self.payload,
            signals=self.signals,
            coupling=self.coupling,
            risk=self.risk,
            ranking=self.ranking,
            meta=meta,
        )
