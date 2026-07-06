import sys

from lentra.ai_control.aider_executor import AiderExecutor
from lentra.core.market_intelligence.graph_v2.graph_selector import build_default_selector


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m lentra.ai_control.aider_cli '<instruction>'")
        raise SystemExit(1)

    instruction = " ".join(sys.argv[1:])

    selector = build_default_selector()
    files = selector.select(instruction)

    executor = AiderExecutor()

    result = executor.full_cycle(
        instruction=instruction,
        files=files
    )

    print(result)


if __name__ == "__main__":
    main()
