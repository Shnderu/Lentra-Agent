"""
DEPRECATED API SERVER WRAPPER
"""

# LEGACY GATEWAY REMOVED
# All execution moved to lentra.core.gateway

def gateway_execute(*args, **kwargs):
    raise RuntimeError(
        "Legacy gateway disabled. Use lentra.core.gateway.FlowGlue"
    )
