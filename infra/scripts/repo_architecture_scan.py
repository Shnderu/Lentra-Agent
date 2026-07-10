import subprocess
import ast
import sys


FORBIDDEN_CLASSES = [
    "EngineRegistryV2",
    "EngineRegistryV3",
    "GraphEngine",
    "WorkflowEngine",
]


def scan_file(path):
    violations = []

    try:
        with open(path, "r") as f:
            tree = ast.parse(f.read(), filename=path)
    except Exception:
        return []

    for node in ast.walk(tree):

        if isinstance(node, ast.ClassDef):

            if node.name in FORBIDDEN_CLASSES:
                violations.append(
                    (path, node.name)
                )

    return violations


def get_python_files():

    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True
    ).stdout.splitlines()

    return [
        f for f in result
        if f.endswith(".py")
    ]


def main():

    violations = []

    for file in get_python_files():
        violations.extend(
            scan_file(file)
        )

    if violations:

        print(
            "\n❌ ARCHITECTURE VIOLATIONS (LAYER 2)\n"
        )

        for path, cls in violations:
            print(
                f"{path} -> {cls}"
            )

        return 1

    print(
        "\n✅ ARCHITECTURE CLEAN (LAYER 2)\n"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
