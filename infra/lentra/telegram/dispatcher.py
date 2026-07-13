"""
Legacy Telegram dispatcher compatibility layer.

Retired:
    direct GatewayV3 initialization

Canonical execution path:
    SearchPipeline -> GatewayV3 -> Engines

Telegram runtime is disabled during architecture restoration.

See:
    docs/AUDIT_CURRENT_STATE_2026-07-13/
"""


class Dispatcher:
    """
    Deprecated compatibility placeholder.

    No runtime gateway initialization allowed here.
    """

    def __init__(self):
        self.gateway = None


def get_gateway():
    """
    Legacy API compatibility.

    Gateway ownership belongs to canonical pipeline only.
    """
    return None
