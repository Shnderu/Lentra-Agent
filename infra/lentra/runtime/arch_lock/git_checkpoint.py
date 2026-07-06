import subprocess
import datetime


class GitCheckpoint:
    def create_snapshot(self, tag_prefix="arch_lock_v14"):
        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        tag = f"{tag_prefix}_{ts}"

        subprocess.run(["git", "add", "-A"], cwd="/opt/lentra/infra")
        subprocess.run(["git", "commit", "-m", f"ARCH LOCK checkpoint {tag}"], cwd="/opt/lentra/infra")

        subprocess.run(["git", "tag", tag], cwd="/opt/lentra/infra")

        return tag
