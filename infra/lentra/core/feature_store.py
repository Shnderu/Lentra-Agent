class FeatureStore:
    """
    DISABLED MEMORY FEEDBACK

    ONLY READ-ONLY CACHE (NO FEEDBACK LOOPS)
    """

    def get(self, key):
        return None

    def set(self, key, value):
        # NO OP (intentionally)
        return True
