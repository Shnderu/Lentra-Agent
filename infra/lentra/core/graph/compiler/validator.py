from lentra.core.graph.compiler.graph_model import ExecutionGraph


class GraphCompilationError(Exception):
    pass


class GraphValidator:

    REQUIRED_STEPS = ["search", "ranking", "aggregation"]

    @staticmethod
    def validate(graph: ExecutionGraph):

        # 1. check required steps
        for step in GraphValidator.REQUIRED_STEPS:
            if step not in graph.nodes:
                raise GraphCompilationError(f"Missing step: {step}")

        # 2. check ordering constraints
        order = ["search", "ranking", "aggregation"]
        keys = list(graph.nodes.keys())

        for i, step in enumerate(order):
            if step not in keys:
                continue
            idx = keys.index(step)
            if idx < i:
                raise GraphCompilationError(
                    f"Invalid order: {step}"
                )

        # 3. ensure no unknown nodes
        for node in graph.nodes:
            if node not in GraphValidator.REQUIRED_STEPS:
                raise GraphCompilationError(f"Unknown node: {node}")

        return True
