import ast
from pathlib import Path
from typing import Set


class ImportParser:


    def parse(
        self,
        path: Path
    ) -> Set[str]:

        imports = set()

        try:

            tree = ast.parse(
                path.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return imports


        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.Import
            ):

                for item in node.names:

                    imports.add(
                        item.name
                    )


            elif isinstance(
                node,
                ast.ImportFrom
            ):

                if node.module:

                    imports.add(
                        node.module
                    )


        return imports
