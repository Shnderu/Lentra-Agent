"""
ARCHITECTURE RULES (ENFORCED BY COMPILER)

Этот модуль заменяет DSL-описание правил на валидную Python-модель.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ArchitectureRule:
    src: str
    dst: str


# =========================
# PIPELINE CONSTRAINTS
# =========================

PIPELINE_MUST_BE_SINGLE: bool = True

ALLOWED_FLOW: List[str] = [
    "search",
    "ranking",
    "aggregation",
]


# =========================
# FORBIDDEN DEPENDENCIES
# =========================
# ранее было DSL:
# FORBIDDEN:
#   lentra.domain -> lentra.services
#
# теперь нормализовано в структуру

FORBIDDEN_IMPORTS: List[ArchitectureRule] = [
    ArchitectureRule(src="lentra/domain", dst="lentra/services"),
    ArchitectureRule(src="lentra/domain", dst="lentra/api"),
    ArchitectureRule(src="lentra/core", dst="lentra/api"),
]


def validate_rule_violation(file_path: str, dep: str) -> bool:
    """
    Проверяет нарушение архитектурного правила.
    """
    for rule in FORBIDDEN_IMPORTS:
        if rule.src in file_path and rule.dst in dep:
            return True
    return False
