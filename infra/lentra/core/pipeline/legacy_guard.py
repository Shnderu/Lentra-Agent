class LegacyPipelineGuard:
    """
    Запрещает использование legacy pipeline entrypoints.

    Используется как мягкий runtime guard (лог + исключение опционально).
    """

    def __init__(self, enabled=True):
        self.enabled = enabled

    def assert_canonical(self, path: str):
        """
        Проверяет, что вызов идёт через canonical pipeline.
        """

        if not self.enabled:
            return

        legacy_signatures = [
            "v1",
            "v2",
            "old_pipeline",
            "dedup_legacy",
            "ranking_legacy",
        ]

        for sig in legacy_signatures:
            if sig in path:
                raise RuntimeError(
                    f"[LEGACY_PIPELINE_BLOCKED] Attempted to use legacy path: {path}"
                )
