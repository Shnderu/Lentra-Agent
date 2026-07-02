import os


class FeatureFlags:

    @staticmethod
        return bool(
            os.getenv("GRAPH_V2_ENABLED", "0") == "1"
        )
