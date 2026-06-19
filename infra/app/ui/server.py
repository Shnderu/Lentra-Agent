"""
CORE LOCKED UI ENTRYPOINT

UI is now static-only and served via API gateway if needed.
Direct runtime execution disabled.
"""
def disabled():
    raise RuntimeError("UI server disabled in CORE LOCK v2")
