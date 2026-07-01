"""
ARCHITECTURE LOCK:
Gateway contract is frozen in V1 mode.
"""

GATEWAY_VERSION = "v1_locked"

ALLOWED_DEPENDENCIES = {
    "orchestrator": "optional"
}

STRICT_MODE = True
