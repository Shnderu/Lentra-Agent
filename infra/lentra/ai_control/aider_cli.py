import sys
from lentra.ai_control.aider_executor import AiderExecutor


def main():
    executor = AiderExecutor()

    instruction = " ".join(sys.argv[1:])

    if not instruction:
        print("No instruction provided")
        return

    result = executor.full_cycle(instruction)

    print("\n=== AIDER EXECUTION COMPLETE ===\n")
    print(result["pre"])
    print(result["result"])
    print(result["post"])


if __name__ == "__main__":
    main()
