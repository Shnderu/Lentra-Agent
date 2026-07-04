from typing import Dict, Any


class ContractFreezeV1:
    """
    HARD CONTRACT LOCK v1.0

    Purpose:
    - prevent schema drift
    - enforce output structure
    - detect unexpected mutations
    """

    VERSION = "v1.0"

    REQUIRED_OUTPUT_KEYS = {
        "dedup",
        "ranking",
        "risk",
        "signals",
        "features"
    }

    REQUIRED_DEDUP_KEYS = {"score", "confidence"}
    REQUIRED_RANKING_KEYS = {"score", "version"}
    REQUIRED_RISK_KEYS = {"risk_level"}

    def validate_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hard validation + repair (non-failing mode)
        """

        # ensure top-level keys
        for key in self.REQUIRED_OUTPUT_KEYS:
            if key not in output:
                output[key] = {}

        # dedup contract
        output["dedup"] = self._ensure_keys(
            output.get("dedup", {}),
            self.REQUIRED_DEDUP_KEYS,
            defaults={"score": 1.0, "confidence": 1.0}
        )

        # ranking contract
        output["ranking"] = self._ensure_keys(
            output.get("ranking", {}),
            self.REQUIRED_RANKING_KEYS,
            defaults={"score": 0.0, "version": "ranking_v2"}
        )

        # risk contract
        output["risk"] = self._ensure_keys(
            output.get("risk", {}),
            self.REQUIRED_RISK_KEYS,
            defaults={"risk_level": 0.0}
        )

        # version stamp
        output["_contract"] = {
            "freeze_version": self.VERSION
        }

        return output

    def detect_drift(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns drift report (non-blocking)
        """

        drift = {
            "missing_keys": [],
            "extra_keys": [],
            "status": "ok"
        }

        for key in self.REQUIRED_OUTPUT_KEYS:
            if key not in output:
                drift["missing_keys"].append(key)

        for key in output.keys():
            if key not in self.REQUIRED_OUTPUT_KEYS and key != "_contract":
                drift["extra_keys"].append(key)

        if drift["missing_keys"] or drift["extra_keys"]:
            drift["status"] = "drift_detected"

        return drift

    def _ensure_keys(self, obj: Dict[str, Any], required: set, defaults: dict):
        for k in required:
            if k not in obj:
                obj[k] = defaults.get(k, None)
        return obj
