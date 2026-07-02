class GraphToggle:
    """
    SAFE OS Graph v2 activation policy
    - controls graph layer execution per request
    """

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def is_enabled(self, payload: dict) -> bool:
        # future: can be request-level routing
