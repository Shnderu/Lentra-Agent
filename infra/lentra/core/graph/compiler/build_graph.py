from lentra.services.pipeline_definition import build_pipeline
from lentra.core.graph.compiler.graph_model import GraphNode, ExecutionGraph


def build_execution_graph():

    pipeline = build_pipeline()

    nodes = {}

    for step in pipeline.steps:
        nodes[step.name] = GraphNode(
            name=step.name,
            deps=[]
        )

    return ExecutionGraph(nodes=nodes)
