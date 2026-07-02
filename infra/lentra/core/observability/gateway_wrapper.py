class ObservabilityGatewayWrapper:
    """
    SAFE PASS-THROUGH WRAPPER

    RULE:
    - NEVER breaks attribute access
    - ALWAYS forwards unknown attrs to inner gateway
    """

    def __init__(self, gateway):
        self.gateway = gateway
        self.watchdog = None
        self.registry = None

    def handle(self, payload):
        return self.gateway.handle(payload)

    def __getattr__(self, item):
        """
        CRITICAL FIX:
        prevents AttributeError crashes in admin layer
        """
        return getattr(self.gateway, item)
