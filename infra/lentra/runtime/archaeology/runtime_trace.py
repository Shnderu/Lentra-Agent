from pathlib import Path
import ast


class RuntimeTrace:


    def __init__(
        self,
        root="."
    ):
        self.root = Path(root)


    def scan_file(
        self,
        file
    ):

        result = {
            "file": str(file),
            "imports": []
        }


        try:

            tree = ast.parse(
                file.read_text(
                    errors="ignore"
                )
            )


            for node in ast.walk(tree):

                if isinstance(
                    node,
                    ast.Import
                ):

                    for item in node.names:
                        result["imports"].append(
                            item.name
                        )


                elif isinstance(
                    node,
                    ast.ImportFrom
                ):

                    if node.module:
                        result["imports"].append(
                            node.module
                        )


        except Exception:

            pass


        return result



    def run(
        self
    ):

        data = []


        for file in self.root.rglob(
            "*.py"
        ):

            data.append(
                self.scan_file(
                    file
                )
            )


        return data
