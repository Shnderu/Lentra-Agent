from __future__ import annotations

import ast
import os
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class SymbolEntry:
    file: str
    symbols: List[str]


class SymbolIndex:
    def __init__(self):
        self.nodes: Dict[str, SymbolEntry] = {}
        self.symbol_index: Dict[str, Dict[str, Any]] = {}


class GraphSymbolIndexer:
    """
    Production symbol indexer for Lentra GraphV2.

    NO runtime scanning.
    ONLY offline build step.
    """

    def __init__(self, root: str = "/opt/lentra/infra/lentra"):
        self.root = root
        self.index = SymbolIndex()

    def build(self) -> SymbolIndex:
        for dirpath, _, filenames in os.walk(self.root):
            for f in filenames:
                if not f.endswith(".py"):
                    continue

                path = os.path.join(dirpath, f)
                self._process_file(path)

        return self.index

    def _process_file(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as fp:
                tree = ast.parse(fp.read(), filename=path)
        except Exception:
            return

        symbols = self._extract_symbols(tree)

        if not symbols:
            return

        node_id = self._infer_node_id(path)

        self.index.nodes[node_id] = SymbolEntry(
            file=path,
            symbols=symbols
        )

        for sym in symbols:
            self.index.symbol_index[sym] = {
                "file": path
            }

    def _extract_symbols(self, tree: ast.AST) -> List[str]:
        symbols = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                symbols.append(node.name)

                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        symbols.append(f"{node.name}.{child.name}")

            elif isinstance(node, ast.FunctionDef):
                symbols.append(node.name)

        return symbols

    def _infer_node_id(self, path: str) -> str:
        if "risk" in path:
            return "risk_engine"
        if "pricing" in path:
            return "pricing_engine"
        if "ranking" in path:
            return "ranking_engine"
        if "dedup" in path:
            return "dedup_engine"
        if "area" in path:
            return "area_engine"

        return os.path.basename(path).replace(".py", "")
