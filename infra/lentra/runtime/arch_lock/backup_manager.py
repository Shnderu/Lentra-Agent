import shutil
import os
import datetime


class BackupManager:
    def create_backup(self, file_path: str):
        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        backup_path = f"{file_path}.bak.{ts}"
        shutil.copy2(file_path, backup_path)

        return backup_path
