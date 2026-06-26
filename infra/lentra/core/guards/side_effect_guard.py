class SideEffectGuard:
    """
    NO SIDE EFFECT ENFORCEMENT ONLY (PASSIVE)
    """

    def validate(self, action):
        return True
