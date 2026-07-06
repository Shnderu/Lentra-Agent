"""
RUNTIME GUARD LAYER

This module enforces architecture rules.
Must NEVER be imported by core.
"""

def check_import(from_module: str, to_module: str):
    forbidden = [
        ("core", "runtime.guard")
    ]

    for f in forbidden:
        if f[0] in from_module and f[1] in to_module:
            raise RuntimeError(f"[ARCH GUARD] {from_module} -> {to_module}")
