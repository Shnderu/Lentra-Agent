class SystemBoundaryGuard:
    """
    PASSIVE VALIDATION ONLY

    НЕ влияет на execution flow
    """

    def check(self, data):
        return {
            "allowed": True,
            "reason": None
        }
