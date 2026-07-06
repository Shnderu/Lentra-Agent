"""
CONTROL PANEL (runtime safe version)

NO FRAMEWORKS ALLOWED HERE
NO FASTAPI
NO HTTP
"""

def get_control_state():
    return {
        "status": "ok",
        "layer": "runtime-control-panel"
    }


def health():
    return {"status": "healthy"}
