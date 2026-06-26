class PolicyEngine:
    """
    POLICY = NON-EXECUTION LAYER

    Только мета-информация.
    Никакого влияния на flow.
    """

    def evaluate(self, *args, **kwargs):
        return {
            "allowed": True,
            "metadata": {}
        }
