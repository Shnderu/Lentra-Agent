IGNORED_PATHS = {
    "__pycache__",
    ".git",
    "venv-bot",
    "venv",
    ".venv",
    "node_modules",
}


def should_index_path(path: str) -> bool:
    normalized = path.replace("\\", "/")

    if normalized.endswith(".pyc"):
        return False

    for ignored in IGNORED_PATHS:
        if f"/{ignored}/" in normalized:
            return False
        if normalized.endswith(f"/{ignored}"):
            return False
        if normalized == ignored:
            return False

    return True
