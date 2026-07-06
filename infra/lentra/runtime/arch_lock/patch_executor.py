from lentra.runtime.arch_lock.backup_manager import BackupManager
from lentra.runtime.arch_lock.ast_rewriter import ASTRewriter


class PatchExecutor:
    def __init__(self):
        self.backup = BackupManager()
        self.rewriter = ASTRewriter()

    def apply_import_patch(self, file_path: str, old: str, new: str):
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        # backup first
        backup_path = self.backup.create_backup(file_path)

        # rewrite AST
        new_source = self.rewriter.rewrite_import(source, old, new)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_source)

        return {
            "file": file_path,
            "backup": backup_path,
            "status": "patched"
        }
