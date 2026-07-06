import ast


class ImportFirewall:
    """
    ARCH LOCK v1 - AST import enforcement layer
    """

    FORBIDDEN_EDGES = [
        ("lentra.core", "lentra.runtime"),
        ("lentra.core", "fastapi"),
        ("lentra.core", "uvicorn"),
        ("lentra.runtime", "lentra.core.bootstrap"),
        ("lentra.api", "lentra.runtime.execution"),
    ]

    def scan_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)

        module_name = file_path.replace("/", ".").replace(".py", "")

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if not node.module:
                    continue

                for frm, to in self.FORBIDDEN_EDGES:
                    if frm in module_name and node.module.startswith(to):
                        raise RuntimeError(
                            f"[ARCH LOCK v1 VIOLATION] {module_name} -> {node.module}"
                        )
