def detect_root_cause(errors, metrics):
    logs = errors.get("logs", "")

    if "Timeout reading from socket" in logs:
        return {"root_cause": "PIPELINE_EXECUTION_STUCK", "severity": "HIGH"}

    if "Name or service not known" in logs:
        return {"root_cause": "REDIS_CONNECTION_FAILURE", "severity": "HIGH"}

    if "ModuleNotFoundError" in logs:
        return {"root_cause": "DEPENDENCY_MISSING", "severity": "CRITICAL"}

    return {"root_cause": "UNKNOWN", "severity": "MEDIUM"}
