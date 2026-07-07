from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class ExecutionJournalV1:
    """
    Persistent execution history for controlled runtime.

    Stores:
    - execution requests
    - plans
    - runtime results
    - verification outcomes
    - checkpoints
    """

    def __init__(
        self,
        storage_path: str = "/opt/lentra/runtime/execution_journal"
    ):
        self.storage = Path(storage_path)
        self.storage.mkdir(
            parents=True,
            exist_ok=True
        )

    def _entry_path(self, execution_id: str) -> Path:
        return self.storage / f"{execution_id}.json"

    def create(
        self,
        query: str,
        payload: Dict[str, Any] | None = None
    ) -> str:

        execution_id = (
            "exec_"
            + uuid.uuid4().hex[:12]
        )

        entry = {
            "id": execution_id,
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),

            "query": query,

            "status": "created",

            "payload": payload or {},

            "events": []
        }

        self._write(
            execution_id,
            entry
        )

        return execution_id


    def append_event(
        self,
        execution_id: str,
        event: str,
        data: Dict[str, Any] | None = None
    ):

        entry = self._read(
            execution_id
        )

        entry["events"].append(
            {
                "timestamp":
                    datetime.now(
                        timezone.utc
                    ).isoformat(),

                "event": event,

                "data": data or {}
            }
        )

        self._write(
            execution_id,
            entry
        )


    def update_status(
        self,
        execution_id: str,
        status: str
    ):

        entry = self._read(
            execution_id
        )

        entry["status"] = status

        self._write(
            execution_id,
            entry
        )


    def get(
        self,
        execution_id: str
    ) -> Dict[str, Any]:

        return self._read(
            execution_id
        )


    def _write(
        self,
        execution_id: str,
        data: Dict[str, Any]
    ):

        path = self._entry_path(
            execution_id
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )


    def _read(
        self,
        execution_id: str
    ) -> Dict[str, Any]:

        path = self._entry_path(
            execution_id
        )

        if not path.exists():
            raise FileNotFoundError(
                execution_id
            )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)
