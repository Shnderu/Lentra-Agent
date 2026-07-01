from typing import Dict, Any


class OutputAssembler:
    """
    Canonical assembler for Market Intelligence output contract.
    Converts raw engine output into UI + API + meta contract.
    """

    def assemble(self, ui: Dict[str, Any], api: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "ui": ui or {},
            "api": api or {},
            "meta": meta or {}
        }
