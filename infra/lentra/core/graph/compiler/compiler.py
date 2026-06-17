from lentra.core.graph.compiler.build_graph import build_execution_graph
from lentra.core.graph.compiler.validator import GraphValidator


class ArchitectureCompiler:

    @staticmethod
    def compile():

        graph = build_execution_graph()

        GraphValidator.validate(graph)

        print("[ARCH COMPILER] graph compilation OK")

        return graph
