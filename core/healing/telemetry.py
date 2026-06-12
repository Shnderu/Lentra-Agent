import subprocess

def collect_metrics():
    try:
        logs = subprocess.getoutput("docker logs --tail 50 lentra-worker")
    except Exception as e:
        logs = str(e)

    return {
        "logs": logs,
        "tasks": 0,
        "results": 0
    }
