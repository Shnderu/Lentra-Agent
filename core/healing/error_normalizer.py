def normalize_errors(metrics):
    return {
        "logs": metrics.get("logs", ""),
        "raw": metrics
    }
