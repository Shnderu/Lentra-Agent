from lentra.ai_control.aider_deterministic_executor import AiderDeterministicExecutor


class RuntimeExecutorAdapterV1:
    """
    Adapter between ControlledRuntime and AiderDeterministicExecutor.

    Keeps execution contract stable.
    """

    def __init__(self):
        self.executor = AiderDeterministicExecutor()

    def build_command(self, prompt: str, files: list[str]):

        command = [
            "aider",
            "--yes-always",
            "--no-suggest-shell-commands",
            "--auto-commits",
        ]

        command.extend(files)

        command.extend(
            [
                "--message",
                prompt
            ]
        )

        return command


    def execute(self, prompt: str, files: list[str]):

        return self.executor.run(
            prompt,
            files
        )
