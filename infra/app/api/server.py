"""
LEGACY ADAPTER LAYER
Forwarding requests to lentra primary system.
"""

from lentra.services.intelligence import handle_request


def legacy_search(payload):
    return handle_request(payload)
