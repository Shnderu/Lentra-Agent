import os

SPEC_PATH = "/opt/flyrum/docs/FlyRum_AI_SPEC.md"

def validate_spec_exists():
    if not os.path.exists(SPEC_PATH):
        raise RuntimeError("FATAL: FlyRum spec missing")

def load_spec():
    with open(SPEC_PATH, "r", encoding="utf-8") as f:
        return f.read()
