class SystemBoundary:
    """
    Single source of truth for system ownership.
    """

    PRIMARY_SYSTEM = "lentra"
    LEGACY_EXECUTION_LAYER = "app.core.graph"

    @staticmethod
    def is_core(module: str) -> bool:
        return module.startswith("lentra.")

    @staticmethod
    def is_legacy(module: str) -> bool:
        return module.startswith("app.core")
