import sys


ALLOWED_IMPORTS = {
    "lentra.services": ["lentra.domain", "lentra.core"],
    "lentra.api": ["lentra.services"],
    "lentra.bot": ["lentra.services"],
    "lentra.domain": [],  # pure layer
}


def check_import(module: str, target: str):
    for prefix, allowed in ALLOWED_IMPORTS.items():
        if module.startswith(prefix):
            for a in allowed:
                if target.startswith(a):
                    return True
            if not allowed:
                return False
    return True


class ImportGuard:
    @staticmethod
    def validate(importer: str, target: str):
        if not check_import(importer, target):
            raise ImportError(
                f"[ARCH GUARD] {importer} cannot import {target}"
            )
