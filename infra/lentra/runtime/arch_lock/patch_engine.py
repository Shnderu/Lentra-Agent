from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Violation:
    source: str
    target: str
    file: str
    rule: str


@dataclass
class Patch:
    file: str
    old: str
    new: str
    confidence: float


class PatchEngine:
    def __init__(self, policy_graph=None):
        self.policy_graph = policy_graph

    def generate_patches(self, violations: List[Violation]) -> List[Patch]:
        result: List[Patch] = []

        for v in violations:
            patch = self._suggest(v)
            if patch:
                result.append(patch)

        return result

    def _suggest(self, v: Violation) -> Optional[Patch]:
        # runtime -> core boundary fix heuristic
        if "runtime" in v.source and "core" in v.target:
            return Patch(
                file=v.file,
                old=v.target,
                new=v.target.replace("runtime", "core"),
                confidence=0.8
            )

        # core -> runtime violation reverse
        if "core" in v.source and "runtime" in v.target:
            return Patch(
                file=v.file,
                old=v.target,
                new=v.target.replace("runtime", "core"),
                confidence=0.6
            )

        return None

    def apply_patch(self, patch: Patch):
        with open(patch.file, "r") as f:
            content = f.read()

        content = content.replace(patch.old, patch.new)

        with open(patch.file, "w") as f:
            f.write(content)
