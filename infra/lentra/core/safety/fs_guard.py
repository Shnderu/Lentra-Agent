# ============================================================
# FILESYSTEM WRITE PROTECTION GATE
# ============================================================

import builtins
import os

BLOCKED_PATTERNS = [
    "cat <<",
    "chmod",
    "chown",
    "chattr",
    ">", 
    ">>",
]


_original_open = builtins.open


def guarded_open(*args, **kwargs):
    path = args[0] if args else ""

    if isinstance(path, str):
        for p in BLOCKED_PATTERNS:
            if p in path:
                raise RuntimeError(f"[FS BLOCKED] dangerous write attempt: {path}")

    return _original_open(*args, **kwargs)


def install_fs_guard():
    builtins.open = guarded_open
