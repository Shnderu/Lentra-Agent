import sys


def validate_imports(module_name: str):
    if module_name.startswith("app.core"):
        raise RuntimeError(
            "[LOCK LEVEL 3] Legacy import detected: app.core is forbidden"
        )
