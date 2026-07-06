from __future__ import annotations

from typing import Dict, Any

from lentra.ai_control.aider_executor import AiderExecutor
from lentra.core.market_intelligence.pipeline.file_scope_resolver import FileScopeResolver


class IntelligencePipelineOrchestrator:

    def __init__(self):
        self.aider = AiderExecutor()
        self.scope_resolver = FileScopeResolver()

    def execute(self, instruction: str, target_file: str, context: Dict[str, Any] | None = None) -> str:
        files = self.scope_resolver.resolve(
            target_file=target_file,
            instruction=instruction,
            context=context,
        )

        return self.aider.full_cycle(
            instruction=instruction,
            files=files
        )
