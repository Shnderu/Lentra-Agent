import ast
import os
from collections import defaultdict


class DependencyGraph:
    def __init__(self):
        self.graph = defaultdict(set)

    def scan_file(self, filepath: str):
        if not filepath.endswith(".py"):
            return

        with open(filepath, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read(), filename=filepath)
            except Exception:
                return

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    self._add(filepath, n.name)

            if isinstance(node, ast.ImportFrom):
                if node.module:
                    self._add(filepath, node.module)

    def _add(self, src: str, dst: str):
        self.graph[src].add(dst)

    def scan_dir(self, root: str):
        for base, _, files in os.walk(root):
            for f in files:
                self.scan_file(os.path.join(base, f))

    def get_graph(self):
        return dict(self.graph)
