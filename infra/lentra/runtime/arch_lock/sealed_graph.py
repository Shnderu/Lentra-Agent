import os
import ast
import json
import hashlib


class SealedGraph:
    """
    Builds immutable import graph snapshot.
    Used for boot-time enforcement.
    """

    def build(self, root: str) -> dict:
        graph = {}

        for dirpath, _, files in os.walk(root):
            for f in files:
                if not f.endswith(".py"):
                    continue

                path = os.path.join(dirpath, f)

                try:
                    with open(path, "r", encoding="utf-8") as file:
                        tree = ast.parse(file.read(), filename=path)

                    imports = []

                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for n in node.names:
                                imports.append(n.name)

                        if isinstance(node, ast.ImportFrom):
                            if node.module:
                                imports.append(node.module)

                    graph[path] = sorted(set(imports))

                except Exception:
                    continue

        return graph

    def fingerprint(self, graph: dict) -> str:
        raw = json.dumps(graph, sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()
