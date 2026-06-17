import os
import signal
import subprocess
import time
import requests


PID_FILE = "/tmp/lentra_api.pid"


class ServiceControl:

    def is_running(self):
        if not os.path.exists(PID_FILE):
            return False

        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())

        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def start_api(self):
        if self.is_running():
            print("[CONTROL] API already running")
            return

        print("[CONTROL] starting API...")

        proc = subprocess.Popen(
            ["python", "-m", "app.api.server"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        with open(PID_FILE, "w") as f:
            f.write(str(proc.pid))

        time.sleep(1)

        if not self.health_check():
            print("[CONTROL] API failed health check")
        else:
            print("[CONTROL] API started OK")

    def stop_api(self):
        if not os.path.exists(PID_FILE):
            print("[CONTROL] no PID file")
            return

        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())

        try:
            os.kill(pid, signal.SIGTERM)
            print("[CONTROL] API stopped")
        except OSError:
            print("[CONTROL] process already dead")

        os.remove(PID_FILE)

    def restart_api(self):
        print("[CONTROL] restarting API...")
        self.stop_api()
        time.sleep(1)
        self.start_api()

    def health_check(self):
        try:
            r = requests.get("http://localhost:8080/health", timeout=2)
            return r.status_code == 200
        except Exception:
            return False
