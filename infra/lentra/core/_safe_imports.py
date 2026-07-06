FORBIDDEN = [
    "lentra.runtime",
    "lentra.api",
    "lentra.observability",
    "lentra.runtime.guard"
]

def validate_import(path: str):
    for f in FORBIDDEN:
        if f in path:
            raise RuntimeError(f"[CORE VIOLATION] forbidden import: {path}")
