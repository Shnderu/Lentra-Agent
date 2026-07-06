import subprocess


class GitGuardV1:
    """
    Ensures deterministic execution state before ANY runtime action.
    """

    def __init__(self, repo_path="/opt/lentra/infra"):
        self.repo_path = repo_path

    def ensure_clean(self):
        p = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )

        if p.stdout.strip():
            raise Exception(
                "Working tree not clean. Commit or auto-checkpoint required before runtime execution."
            )
