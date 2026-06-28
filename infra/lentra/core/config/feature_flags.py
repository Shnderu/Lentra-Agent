import os


class FeatureFlags:
    """
    Central feature toggle system.

    Controls pipeline versioning:
    - v1: legacy stable pipeline
    - v2: experimental intelligence pipeline
    """

    @staticmethod
    def use_v2_pipeline() -> bool:
        return os.getenv("LENTRA_PIPELINE_V2", "false").lower() == "true"

    @staticmethod
    def use_v2_dedup() -> bool:
        return os.getenv("LENTRA_V2_DEDUP", "true").lower() == "true"

    @staticmethod
    def use_v2_risk() -> bool:
        return os.getenv("LENTRA_V2_RISK", "true").lower() == "true"

    @staticmethod
    def use_v2_ranking() -> bool:
        return os.getenv("LENTRA_V2_RANKING", "true").lower() == "true"
