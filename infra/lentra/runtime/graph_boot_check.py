from lentra.core.guards.graph_fingerprint import compute_flowglue_signature


EXPECTED_HASH = "LOCKED_PLACEHOLDER_HASH"


def validate_graph():
    current = compute_flowglue_signature()

    if current != EXPECTED_HASH:
        raise RuntimeError(
            "[SEAL] GRAPH FROZEN - CHANGE DETECTED"
        )
