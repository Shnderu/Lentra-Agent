import sys

from lentra.ai_control.aider_executor import AiderExecutor


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m lentra.ai_control.aider_cli '<instruction>' [files...]")
        raise SystemExit(1)

    instruction = sys.argv[1]
    files = sys.argv[2:] if len(sys.argv) > 2 else []

    executor = AiderExecutor()
    result = executor.full_cycle(instruction, files)

    print(result)


if __name__ == "__main__":
    main()
