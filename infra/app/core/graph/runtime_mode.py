"""
GraphEngine is now OBSERVABILITY ONLY.
"""

RUNTIME_MODE = "observability"

def is_execution_enabled():
    return False


def is_tracing_enabled():
    return True
