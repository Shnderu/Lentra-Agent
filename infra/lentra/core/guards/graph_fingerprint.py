import hashlib
import inspect
from lentra.core.gateway.flow_glue import FlowGlue


def compute_flowglue_signature() -> str:
    """
    Creates deterministic fingerprint of DI graph.
    """

    source = inspect.getsource(FlowGlue)

    return hashlib.sha256(source.encode()).hexdigest()


def assert_graph_unchanged(expected_hash: str):
    current = compute_flowglue_signature()

    if current != expected_hash:
        raise RuntimeError(
            "[ARCHITECTURE SEAL] DI GRAPH MODIFIED"
        )
