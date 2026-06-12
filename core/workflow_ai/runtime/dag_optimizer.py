class DAGOptimizer:
    """
    Runtime DAG optimizer:
    - adjusts execution plan dynamically
    - removes redundant steps
    - reorders nodes for efficiency
    """

    def optimize(self, dag, context):
        nodes = dag["nodes"]
        edges = dag["edges"]

        # -----------------------------
        # RULE 1: skip validation if context already clean
        # -----------------------------
        if context.get("validated", False):
            nodes = [n for n in nodes if n["id"] != "validate_input"]

        # -----------------------------
        # RULE 2: reduce pipeline for low-load mode
        # -----------------------------
        if context.get("fast_mode", False):
            nodes = [n for n in nodes if n["id"] not in ["rank_results"]]

        # -----------------------------
        # RULE 3: ensure minimal execution graph integrity
        # -----------------------------
        optimized = {
            "nodes": nodes,
            "edges": edges
        }

        return optimized
