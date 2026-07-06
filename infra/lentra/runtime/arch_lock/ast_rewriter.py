import ast


class ASTRewriter:
    """
    Safe AST transformations for ARCH LOCK v1.5
    """

    def rewrite_import(self, source: str, old: str, new: str) -> str:
        tree = ast.parse(source)

        class Transformer(ast.NodeTransformer):
            def visit_ImportFrom(self, node):
                if node.module and node.module.startswith(old):
                    node.module = node.module.replace(old, new)
                return node

        new_tree = Transformer().visit(tree)
        return ast.unparse(new_tree)
