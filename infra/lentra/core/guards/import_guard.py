import sys


BLOCKED_PREFIXES = (
    "app.core",
    "app.",
)


class ImportGuard:
    """
    Runtime import firewall.
    Блокирует legacy import в момент исполнения.
    """

    def install(self):
        sys.meta_path.insert(0, self)

    def find_spec(self, fullname, path, target=None):
        for prefix in BLOCKED_PREFIXES:
            if fullname.startswith(prefix):
                raise ImportError(
                    f"[ARCHITECTURE SEAL] BLOCKED IMPORT: {fullname}"
                )
        return None
