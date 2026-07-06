import subprocess
import sys
from architecture_policy import check_diff


def get_git_diff_all() -> str:
    staged = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True,
        text=True
    ).stdout

    unstaged = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True
    ).stdout

    return staged + "\n" + unstaged


def main():
    diff = get_git_diff_all()

    if not diff.strip():
        print("No changes detected (staged + unstaged)")
        return 0

    violations = check_diff(diff)

    if violations:
        print("\n❌ ARCHITECTURE VIOLATION DETECTED:\n")
        for v in violations:
            print(f" - {v}")

        print("\nCommit blocked by AI diff validator.")
        return 1

    print("✅ Architecture OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
