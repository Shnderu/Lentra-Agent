class EngineIsolator:
    """
    MVP isolator layer for intelligence engines.
    Keeps registry of engines and provides safe access layer.
    """

    def __init__(self, engines=None):
        # engines is expected to be dict or list of engine instances
        self.engines = engines or {}

    def get_engine(self, name: str):
        """
        Safe access to engine by name.
        """
        if isinstance(self.engines, dict):
            return self.engines.get(name)
        return None

    def list_engines(self):
        """
        Return available engines.
        """
        if isinstance(self.engines, dict):
            return list(self.engines.keys())
        return []

    def execute(self, name: str, payload: dict):
        """
        Minimal execution wrapper (MVP stub).
        """
        engine = self.get_engine(name)
        if not engine:
            return {
                "status": "error",
                "error": f"engine_not_found:{name}"
            }

        if hasattr(engine, "run"):
            return engine.run(payload)

        return {
            "status": "error",
            "error": f"engine_has_no_run:{name}"
        }
