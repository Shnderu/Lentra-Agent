from typing import Any, Dict


class EngineIsolator:
    def __init__(self, engines: Dict[str, Any] | None = None):
        # SAFE DEFAULT: NEVER FAIL BOOT
        self.engines = engines if engines is not None else {}

    def get(self, name: str):
        return self.engines.get(name)

    def list(self):
        return list(self.engines.keys())
