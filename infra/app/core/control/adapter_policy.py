"""
Defines adapter isolation rules.
"""

ALLOW_LEGACY_ADAPTERS = True

LEGACY_MODULES = [
    "app.api",
    "app.core.handlers"
]

PRIMARY_MODULE = "lentra"
