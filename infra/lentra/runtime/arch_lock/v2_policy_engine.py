
import ast
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Violation:
    file: str
    rule: str
    target: str


class ArchPolicyV2:
    """
    CORE RULE ENGINE (unchanged)
    """

    def __init__(self, rules: dict):
        self.rules = rules

    def check_file(self, file_path: str, source: str) -> List[Violation]:
        tree = ast.parse(source, filename=file_path)
        violations = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""

                for rule_name, rule in self.rules.items():
                    if rule.get("deny_prefix") and module.startswith(rule["deny_prefix"]):
                        violations.append(
                            Violation(
                                file=file_path,
                                rule=rule_name,
                                target=module,
                            )
                        )

        return violations


class PolicyEngine:
    """
    COMPATIBILITY LAYER FOR ARCH LOCK v2 RUNNER
    """

    def __init__(self, rules: Dict[str, Any] | None = None):
        self.core = ArchPolicyV2(rules or {
            "default_deny_runtime_to_core": {
                "deny_prefix": "lentra.runtime"
            }
        })

    def evaluate(self, violations):
        # annotate only (no filtering)
        return [
            {
                "violation": v,
                "rule": getattr(v, "rule", "unknown"),
                "file": getattr(v, "file", None),
                "target": getattr(v, "target", None),
                "severity": "medium"
            }
            for v in violations
        ]

    def scan_file(self, file_path: str, source: str):
        return self.core.check_file(file_path, source)

