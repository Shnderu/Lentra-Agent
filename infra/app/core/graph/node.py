from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class GraphNode:
    name: str
    handler: Callable
    next_node: Optional[str] = None
