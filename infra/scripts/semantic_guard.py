import subprocess


ALLOWED_ARCHITECTURE = """
Lentra is a single Market Intelligence OS.
No graph execution engines allowed.
No multiple registries.
No orchestration frameworks.
"""


def get_diff():
    return subprocess.run(
        ["git", "diff", "HEAD"],
        capture_output=True,
        text=True
    ).stdout


def main():
    diff = get_diff()

    # simple semantic heuristic (can be upgraded to LLM later)
    forbidden_signals = [
        "new EngineRegistry",
        "class .*V[0-9]",
        "Graph",
        "DAG",
    ]

    for sig in forbidden_signals:
        if sig.lower() in diff.lower():
            print("❌ Semantic architecture violation detected")
            return 1

    print("✅ Semantic OK")
    return 0


if __name__ == "__main__":
    exit(main())
