import sys

from lentra.ai_control.aider_executor import AiderExecutor
from lentra.core.market_intelligence.graph_v2.graph_builder import GraphV2Builder


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m lentra.ai_control.aider_cli '<instruction>'")
        raise SystemExit(1)

    instruction = " ".join(sys.argv[1:])

    # AI-controlled file selection via graph_v2
    graph = GraphV2Builder()
    selected_files = graph.select_files(instruction)

    executor = AiderExecutor()

    result = executor.full_cycle(
        instruction=instruction,
        files=selected_files
    )

    print(result)


if __name__ == "__main__":
    main()
