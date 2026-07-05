from typing import Dict, Any, Mapping
from copy import deepcopy


class ImmutableContextError(Exception):
    pass


class MarketContext:
    """
    STEP 1.1 — IMMUTABLE CONTEXT CORE

    RULES:
    - ctx is immutable from external usage
    - no in-place mutation allowed
    - transformations return NEW instances
    """

    def __init__(self, payload: Dict[str, Any]):
        self._raw: Mapping[str, Any] = deepcopy(payload)
        self._state: Dict[str, Any] = deepcopy(payload)
        self._frozen: bool = False

    # -------------------------
    # READ
    # -------------------------
    def get(self) -> Dict[str, Any]:
        return deepcopy(self._state)

    def raw(self) -> Mapping[str, Any]:
        return self._raw

    # -------------------------
    # PURE TRANSFORM
    # -------------------------
    def derive(self, **updates) -> "MarketContext":
        new_state = deepcopy(self._state)
        new_state.update(updates)
        return MarketContext(new_state)

    # -------------------------
    # FREEZE
    # -------------------------
    def freeze(self) -> None:
        self._frozen = True

    def assert_not_frozen(self):
        if self._frozen:
            raise ImmutableContextError("Context is frozen")

    # -------------------------
    # FORBIDDEN MUTATIONS
    # -------------------------
    def set(self, key: str, value: Any):
        self.assert_not_frozen()
        raise ImmutableContextError("Direct mutation forbidden")

    def update(self, data: Dict[str, Any]):
        self.assert_not_frozen()
        raise ImmutableContextError("Direct update forbidden")
