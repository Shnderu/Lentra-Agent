from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Snapshot:
    objects: List[Dict]


@dataclass
class AIContext:
    title: str
    snapshot: Snapshot
