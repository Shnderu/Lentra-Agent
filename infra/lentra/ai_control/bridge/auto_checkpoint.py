import subprocess
from datetime import datetime


class AutoCheckpoint:
    """
    Ensures git working tree is clean before execution.
    If dirty → auto-commits with deterministic message.
    """

    def __init__(self, repo_root: str = "/opt/lentra"):
        self.repo_root = repo_root

    def _is_dirty(self) -> bool:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )
        return len(result.stdout.strip()) > 0

    def _commit(self):
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        subprocess.run(["git", "add", "-A"], cwd=self.repo_root, check=True)

        subprocess.run(
            ["git", "commit", "-m", f"auto-checkpoint: bridge execution {timestamp}"],
            cwd=self.repo_root,
            check=True,
        )

    def ensure_clean(self):
        if self._is_dirty():
            self._commit()

        # final validation
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )

        if result.stdout.strip():
            raise Exception("AutoCheckpoint failed: repo still dirty")
