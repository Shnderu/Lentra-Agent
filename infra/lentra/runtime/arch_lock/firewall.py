import ast
from typing import List, Tuple


class Firewall:
    """
    ARCH LOCK v1.6
    Static AST-based violation detector
    """

    def __init__(self, rules: List[Tuple[str, str]]):
        # (from_module, forbidden_to_module)
        self.rules = rules

    def scan_file(self, file_path: str):
        with open(file_path, "r") as f:
            source = f.read()

        tree = ast.parse(source, filename=file_path)

        violations = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for rule_from, rule_to in self.rules:
                    if rule_from in file_path and rule_to in module:
                        violations.append({
                            "file": file_path,
                            "from": rule_from,
                            "to": rule_to
                        })

        return violations

    def scan(self, project_root: str):
        import os

        all_violations = []

        for root, _, files in os.walk(project_root):
            for f in files:
                if f.endswith(".py"):
                    path = os.path.join(root, f)
                    all_violations.extend(self.scan_file(path))

        return all_violations
