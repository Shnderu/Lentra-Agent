import os
import signal
import subprocess
import time
import requests


API_PID = "/tmp/lentra_api.pid"
UI_PID = "/tmp/lentra_ui.pid"


class Orchestrator:

    # -------------------------
    # INTERNAL HELPERS
    # -------------------------

    def _is_alive(self, pid_file):
        if not os.path.exists(pid_file):
            return False

        with open(pid_file, "r") as f:
            pid = int(f.read().strip())

        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def _write_pid(self, pid_file, pid):
        with open(pid_file, "w") as f:
            f.write(str(pid))

    def _stop(self, pid_file, name):
        if not os.path.exists(pid_file):
            print(f"[ORCH] {name} not running")
            return

        with open(pid_file, "r") as f:
            pid = int(f.read().strip())

        try:
            os.kill(pid, signal.SIGTERM)
            print(f"[ORCH] {name} stopped")
        except OSError:
            print(f"[ORCH] {name} already dead")

        os.remove(pid_file)

    # -------------------------
    # HEALTH
    # -------------------------

    def api_health(self):
        try:
            r = requests.get("http://localhost:8080/health", timeout=2)
            return r.status_code == 200
        except Exception:
            return False

    def ui_health(self):
        try:
            r = requests.get("http://localhost:3000", timeout=2)
            return r.status_code == 200
        except Exception:
            return False

    # -------------------------
    # START
    # -------------------------

    def start_api(self):
        if self._is_alive(API_PID):
            print("[ORCH] API already running")
            return

        proc = subprocess.Popen(
            ["python", "-m", "app.api.server"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self._write_pid(API_PID, proc.pid)
        time.sleep(1)

        if self.api_health():
            print("[ORCH] API started OK")
        else:
            print("[ORCH] API failed health check")

    def start_ui(self):
        if self._is_alive(UI_PID):
            print("[ORCH] UI already running")
            return

        proc = subprocess.Popen(
            ["python", "-m", "app.ui.server"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self._write_pid(UI_PID, proc.pid)
        time.sleep(1)

        if self.ui_health():
            print("[ORCH] UI started OK")
        else:
            print("[ORCH] UI failed health check")

    # -------------------------
    # STOP
    # -------------------------

    def stop_api(self):
        self._stop(API_PID, "API")

    def stop_ui(self):
        self._stop(UI_PID, "UI")

    def stop_all(self):
        print("[ORCH] stopping all services...")
        self.stop_ui()
        self.stop_api()

    # -------------------------
    # START ALL
    # -------------------------

    def start_all(self):
        print("[ORCH] starting full system...")

        self.start_api()
        self.start_ui()

        print("[ORCH] system started")

    # -------------------------
    # RESTART
    # -------------------------

    def restart_all(self):
        print("[ORCH] restarting full system...")

        self.stop_all()
        time.sleep(1)
        self.start_all()

    # -------------------------
    # STATUS
    # -------------------------

    def status(self):
        return {
            "api_running": self._is_alive(API_PID),
            "ui_running": self._is_alive(UI_PID),
            "api_health": self.api_health(),
            "ui_health": self.ui_health()
        }
