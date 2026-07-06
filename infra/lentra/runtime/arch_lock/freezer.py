import os
import hashlib
import ast


class GraphFreezer:
    """
    Creates immutable hash of architecture graph.
    Prevents drift in runtime/core boundaries.
    """

    def hash_file(self, path: str) -> str:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def scan(self, root: str) -> dict:
        result = {}

        for dirpath, _, files in os.walk(root):
            for f in files:
                if not f.endswith(".py"):
                    continue

                path = os.path.join(dirpath, f)

                try:
                    with open(path, "r", encoding="utf-8") as file:
                        ast.parse(file.read(), filename=path)
                    result[path] = self.hash_file(path)
                except Exception:
                    # skip invalid files (arch lock already handles syntax)
                    continue

        return result
