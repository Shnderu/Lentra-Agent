from pathlib import Path
from typing import List


EXCLUDED = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
}


class RepositoryScanner:

    def __init__(
        self,
        root: str
    ):

        self.root = Path(root)


    def scan(self) -> List[Path]:

        result = []

        for path in self.root.rglob(
            "*.py"
        ):

            if any(
                part in EXCLUDED
                for part in path.parts
            ):
                continue

            result.append(
                path
            )

        return result
