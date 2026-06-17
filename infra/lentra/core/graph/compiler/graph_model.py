from dataclasses import dataclass
from typing import Dict, List


@dataclass
class GraphNode:
    name: str
    deps: List[str]


@dataclass
class ExecutionGraph:
    nodes: Dict[str, GraphNode]
