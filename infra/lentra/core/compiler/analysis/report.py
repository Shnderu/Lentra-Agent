class ArchitectureReport:

    @staticmethod
    def generate(graph: dict):

        total_files = len(graph)
        total_edges = sum(len(v) for v in graph.values())

        return {
            "files": total_files,
            "dependencies": total_edges,
            "status": "OK"
        }
