import subprocess
import datetime


class GitWorkflow:
    def create_branch(self):
        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        branch = f"arch-lock-v15-{ts}"

        subprocess.run(["git", "checkout", "-b", branch], cwd="/opt/lentra/infra")

        return branch

    def commit(self, message: str):
        subprocess.run(["git", "add", "-A"], cwd="/opt/lentra/infra")
        subprocess.run(["git", "commit", "-m", message], cwd="/opt/lentra/infra")

        return True
