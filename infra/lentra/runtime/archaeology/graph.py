from typing import Dict

from .models import ModuleNode
from .parser import ImportParser


class ImportGraph:


    def __init__(self):

        self.nodes: Dict[str, ModuleNode] = {}

        self.module_index: Dict[str, str] = {}

        self.resolve_cache = {}

        self.parser = ImportParser()



    def build(
        self,
        files
    ):

        for file in files:

            key = str(file)

            node = ModuleNode(
                path=key
            )

            node.imports = self.parser.parse(
                file
            )

            self.nodes[key] = node


            module_name = (
                key
                .replace(
                    "/opt/lentra/infra/",
                    ""
                )
                .replace(
                    "/",
                    "."
                )
                .replace(
                    ".py",
                    ""
                )
            )


            self.module_index[
                module_name
            ] = key


        return self



    def _resolve(
        self,
        imported: str
    ):

        if imported in self.resolve_cache:

            return self.resolve_cache[imported]


        result = set()


        direct = self.module_index.get(
            imported
        )


        if direct:

            result.add(
                direct
            )


        prefix = imported + "."


        for module_name, path in self.module_index.items():

            if module_name.startswith(
                prefix
            ):

                result.add(
                    path
                )


        self.resolve_cache[
            imported
        ] = result


        return result



    def link(self):

        print(
            "[ARCH] linking graph..."
        )


        for source, node in self.nodes.items():

            resolved = set()


            for imported in node.imports:

                resolved.update(
                    self._resolve(
                        imported
                    )
                )


            node.imports = resolved


            for target in resolved:

                target_node = self.nodes.get(
                    target
                )


                if target_node:

                    target_node.imported_by.add(
                        source
                    )


        return self
