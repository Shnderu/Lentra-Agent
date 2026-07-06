import subprocess
import sys
from architecture_policy import check_diff


def get_diff():
    staged = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True).stdout
    unstaged = subprocess.run(["git", "diff"], capture_output=True, text=True).stdout
    return staged + unstaged


def main():
    diff = get_diff()

    if not diff.strip():
        return 0

    violations = check_diff(diff)

    if violations:
        print("\n❌ ARCHITECTURE VIOLATION (LAYER 1)\n")
        for v in violations:
            print(" -", v)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
