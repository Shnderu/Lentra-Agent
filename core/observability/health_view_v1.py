import json
from core.observability.state_reconstructor_v1 import reconstruct_state

"""
Lentra Observable Core v1
Unified Health View
"""


def health():
    state = reconstruct_state()

    if state["lag"] > 10:
        state["status"] = "DEGRADED"
    elif state["events"] == 0:
        state["status"] = "NO_SIGNAL"
    else:
        state["status"] = "OK"

    return state


if __name__ == "__main__":
    print(json.dumps(health(), indent=2))
