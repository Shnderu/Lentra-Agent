FORBIDDEN_IMPORTS = [
    "runtime",
    "observability",
    "trace",
    "metrics",
    "instrumentation"
]


def assert_core_clean(import_path: str):
    for f in FORBIDDEN_IMPORTS:
        if f in import_path:
            raise RuntimeError(f"[CORE BOUNDARY VIOLATION] {import_path}")
