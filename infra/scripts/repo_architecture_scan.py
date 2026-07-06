import subprocess
import ast
import os
import sys


FORBIDDEN = [
    "EngineRegistryV2",
    "EngineRegistryV3",
    "GraphEngine",
    "WorkflowEngine",
]


def scan_file(path):
    try:
        with open(path, "r") as f:
            content = f.read()
    except:
        return []

    violations = []

    for f in FORBIDDEN:
        if f in content:
            violations.append((path, f))

    return violations


def get_python_files():
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True
    ).stdout.splitlines()

    return [f for f in result if f.endswith(".py")]


def main():
    violations = []

    for file in get_python_files():
        violations.extend(scan_file(file))

    if violations:
        print("\n❌ ARCHITECTURE VIOLATIONS (LAYER 2)\n")
        for v in violations:
            print(f"{v[0]} -> {v[1]}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
