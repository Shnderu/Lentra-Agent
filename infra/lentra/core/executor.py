"""
COMPAT LAYER v1
Execution entrypoint stub

DO NOT EXPAND ARCHITECTURE.
This is a temporary bridge until Scenario Engine fully replaces legacy execution graph.
"""

def execute_scenario(payload: dict):
    """
    Unified execution entrypoint (temporary stub)
    """
    return {
        "status": "ok",
        "mode": "compat_v1",
        "input": payload,
        "note": "executor is not implemented yet, routed via compatibility layer"
    }
