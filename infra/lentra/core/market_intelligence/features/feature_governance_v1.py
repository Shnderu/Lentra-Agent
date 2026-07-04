class FeatureGovernanceV1:
    """
    Feature Governance v1 (STABLE CONTRACT MODE)

    Purpose:
    - no enforcement logic required for v1 freeze
    - only schema passthrough + validation stub
    """

    def __init__(self, config=None):
        self.config = config or {}

    def enforce(self, data):
        """
        Backward compatibility stub
        """
        return data

    def apply(self, data):
        return self.enforce(data)
