from .scanner import RepositoryScanner
from .graph import ImportGraph
from .entrypoints import EntrypointDetector
from .reachability import ReachabilityAnalyzer
from .reporter import ArchaeologyReporter
from .classifier import ArchitectureClassifier
from .domain_classifier import DomainClassifier



class ArchaeologyEngine:


    def __init__(
        self,
        root: str
    ):
        self.root = root



    def run(self):

        print(
            "[ARCH] scanning..."
        )


        files = RepositoryScanner(
            self.root
        ).scan()


        print(
            "[ARCH] files:",
            len(files)
        )


        graph = ImportGraph()

        graph.build(
            files
        ).link()


        print(
            "[ARCH] detecting entrypoints..."
        )


        entrypoints = EntrypointDetector().detect(
            graph.nodes.keys()
        )


        print(
            "[ARCH] entrypoints:",
            len(entrypoints)
        )


        reachable = ReachabilityAnalyzer().analyze(
            graph,
            entrypoints
        )


        report = ArchaeologyReporter().build(
            graph,
            reachable
        )


        report["architecture"] = ArchitectureClassifier().classify(
            files
        )


        report["domains"] = DomainClassifier().classify(
            files
        )


        return report
