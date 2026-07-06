"""
Lentra AI Control Layer - Aider Gateway
Точка входа всех AI-изменений системы через Aider.
"""

import subprocess
from pathlib import Path
from .change_policy import ChangePolicy


class AiderGateway:
    """
    Единственный разрешённый вход для AI изменений кода.
    """

    def __init__(self, repo_path: str = "/opt/lentra/infra"):
        self.repo_path = Path(repo_path)

    def run_task(self, task: str, files: list[str] = None) -> str:
        """
        Выполняет задачу через Aider с применением политик.
        """

        # 1. Проверка политики
        if not ChangePolicy.is_change_allowed(task):
            raise Exception("Task violates architecture policy")

        # 2. Формируем prompt
        safe_prompt = ChangePolicy.enforce_prompt(task)

        # 3. Базовая команда Aider
        cmd = [
            "aider",
            "--yes",
            "--no-auto-commit",
            "--message",
            safe_prompt,
        ]

        # 4. Добавляем файлы контекста (если есть)
        if files:
            for f in files:
                cmd.append(f)

        # 5. Запуск
        process = subprocess.run(
            cmd,
            cwd=str(self.repo_path),
            capture_output=True,
            text=True
        )

        if process.returncode != 0:
            raise Exception(f"Aider failed: {process.stderr}")

        return process.stdout


if __name__ == "__main__":
    gateway = AiderGateway()
    print(gateway.run_task("improve risk scoring stability"))
