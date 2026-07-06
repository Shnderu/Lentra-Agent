import sys

from lentra.ai_control.graph_aider_bridge import GraphAiderBridge


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m lentra.ai_control.graph_aider_bridge_cli '<instruction>'")
        raise SystemExit(1)

    instruction = sys.argv[1]

    bridge = GraphAiderBridge()
    result = bridge.run(instruction)

    print(result)


if __name__ == "__main__":
    main()
