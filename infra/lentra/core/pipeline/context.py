from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class Snapshot:
    objects: List[Any] = field(default_factory=list)


@dataclass
class PipelineContext:
    query: str
    snapshot: Snapshot
    meta: dict = field(default_factory=dict)

    @staticmethod
    def empty(query: str):
        return PipelineContext(
            query=query,
            snapshot=Snapshot(objects=[]),
            meta={}
        )
