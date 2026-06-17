import re
from pathlib import Path

SHELL_PATTERNS = [
    r"cat\s+<<\s*'EOF'",
    r">\s*/opt/",
    r"#!/bin/bash",
]

def is_malicious(content: str) -> bool:
    return any(re.search(p, content) for p in SHELL_PATTERNS)

def safe_write(path: str, content: str):
    if is_malicious(content):
        raise RuntimeError(f"[SAFE_WRITER] Blocked shell injection into {path}")

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    p.write_text(content, encoding="utf-8")
