import importlib
import time

"""
Import Guard v1

Защита от:
- missing dependency crashes
- partial runtime imports
- silent failures
"""

REQUIRED_MODULES = [
    "redis",
    "aiogram",
    "httpx",
    "psycopg2"
]


def validate_imports():
    missing = []

    for module in REQUIRED_MODULES:
        try:
            importlib.import_module(module)
        except Exception:
            missing.append(module)

    if missing:
        print(">>> IMPORT GUARD FAILED")
        print("Missing modules:", missing)
        raise RuntimeError(f"Missing dependencies: {missing}")

    print(">>> IMPORT GUARD OK")
    return True


if __name__ == "__main__":
    validate_imports()
