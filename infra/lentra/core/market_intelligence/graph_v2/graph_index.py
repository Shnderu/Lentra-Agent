from dataclasses import dataclass


@dataclass(frozen=True)
class GraphIndex:
    """
    Immutable routing index.
    Replaces implicit selector state.
    """

    nodes: dict

    def get_node(self, key: str):
        return self.nodes.get(key)

    def has(self, key: str) -> bool:
        return key in self.nodes
