from typing import Dict, Any, Optional


class DomainCoreV1:
    """
    Core domain layer for Lentra.

    NOTE:
    This file must remain pure Python.
    No shell scripts, no heredoc injections.
    """

    def __init__(self):
        self.state: Dict[str, Any] = {}

    def init(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.state["config"] = config or {}
        self.state["initialized"] = True

    def get_state(self) -> Dict[str, Any]:
        return self.state

    def set(self, key: str, value: Any) -> None:
        self.state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)

    def reset(self) -> None:
        self.state.clear()
        self.state["initialized"] = False


def build_domain_core(config: Optional[Dict[str, Any]] = None) -> DomainCoreV1:
    core = DomainCoreV1()
    core.init(config=config)
    return core
