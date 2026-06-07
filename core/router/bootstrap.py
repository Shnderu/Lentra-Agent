"""
Bootstrap layer:
- imports all handlers
- triggers registration
- avoids circular imports
"""

from core.handlers import test  # noqa: F401
