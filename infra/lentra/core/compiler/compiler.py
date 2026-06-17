from lentra.core.compiler.analysis.dependency_graph import DependencyGraph
from lentra.core.compiler.validation.cycle_detector import CycleDetector
from lentra.core.compiler.validation.rule_checker import RuleChecker


class ArchitectureCompiler:

    @staticmethod
    def compile(root="lentra"):

        print("[COMPILER] building dependency graph...")

        graph_builder = DependencyGraph()
        graph = graph_builder.build_from_dir(root)

        print("[COMPILER] checking cycles...")
        CycleDetector(graph).validate()

        print("[COMPILER] checking rules...")
        RuleChecker.validate(graph)

        print("[COMPILER] OK - architecture is valid")

        return graph
