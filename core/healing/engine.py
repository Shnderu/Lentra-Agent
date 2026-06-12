import json
import time

from core.healing.telemetry import collect_metrics
from core.healing.error_normalizer import normalize_errors
from core.healing.root_cause_engine import detect_root_cause
from core.healing.advisor import generate_advice


def run_healing_cycle():
    metrics = collect_metrics()
    errors = normalize_errors(metrics)

    diagnosis = detect_root_cause(errors, metrics)
    advice = generate_advice(diagnosis, metrics)

    report = {
        "timestamp": time.time(),
        "metrics": metrics,
        "diagnosis": diagnosis,
        "advisor": advice
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    run_healing_cycle()
