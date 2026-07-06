"""
CORE BOOTSTRAP (CLEAN)

RULE:
- NO runtime imports
- NO observability imports
- only pure initialization hooks
"""

def init_core():
    """
    Initializes pure domain layer only
    """
    from .executor import Executor

    return Executor()
