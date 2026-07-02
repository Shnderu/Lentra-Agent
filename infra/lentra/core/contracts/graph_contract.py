from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class GraphV2Context:
    enabled: bool = False
    payload: Optional[Dict[str, Any]] = None


def extract_graph_flag(request: Dict[str, Any]) -> GraphV2Context:
    """
    SAFE feature toggle layer:
    - NEVER changes core pipeline
    - only annotates context
    """

    return GraphV2Context(
    )
