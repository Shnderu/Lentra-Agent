import os
import ast
from collections import defaultdict


class DependencyGraph:

    def __init__(self):
        self.graph = defaultdict(set)

    def add_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    self.graph[file_path].add(n.name)

            if isinstance(node, ast.ImportFrom):
                if node.module:
                    self.graph[file_path].add(node.module)

    def build_from_dir(self, root: str):
        for dirpath, _, files in os.walk(root):
            for file in files:
                if file.endswith(".py"):
                    self.add_file(os.path.join(dirpath, file))

        return self.graph
