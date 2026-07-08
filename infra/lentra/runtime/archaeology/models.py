from dataclasses import dataclass, field
from typing import Set


@dataclass
class ModuleNode:

    path: str

    imports: Set[str] = field(
        default_factory=set
    )

    imported_by: Set[str] = field(
        default_factory=set
    )
