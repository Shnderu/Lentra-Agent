from collections import defaultdict
from dataclasses import dataclass


@dataclass
class NodeResult:
    node: str
    data: dict


class ExecutionGraphRuntimeV1:

    def __init__(self):
        self.edges = defaultdict(list)

    def add_edge(self, src, dst):
        self.edges[src].append(dst)

    def execute(self, intent, scenario_executor):
        """
        DAG execution (v1)
        """

        visited = set()
        results = []

        def run(node):
            if node in visited:
                return

            visited.add(node)

            # execute scenario node
            result = scenario_executor.execute_node(intent, node)

            results.append(NodeResult(node=node, data=result))

            for nxt in self.edges[node]:
                run(nxt)

        # entry point
        start = intent.scenarios[0] if hasattr(intent, "scenarios") else "default_scenario_v1"

        run(start)

        return {
            "entry": start,
            "trace": [r.node for r in results],
            "results": [
                {"node": r.node, "data": r.data}
                for r in results
            ]
        }


graph_runtime = ExecutionGraphRuntimeV1()
