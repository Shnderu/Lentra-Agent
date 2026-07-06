# infra/lentra/core/market_intelligence/_import_safety.py

IGNORED_PATHS = {
    "__pycache__",
    ".git",
    "venv-bot",
    "venv",
    ".venv",
    "node_modules",
    "lib",
}

def should_index_path(path: str) -> bool:
    lowered = path.lower()

    for ignored in IGNORED_PATHS:
        if f"/{ignored}/" in lowered or lowered.endswith(ignored):
            return False

    if lowered.endswith(".pyc"):
        return False

    return True
