# LENTRA DIAG TOOL MVP

import subprocess
import sys

DB_NAME = "lentra"
DB_USER = "postgres"

def run(cmd):
    return subprocess.getoutput(cmd)

def queue():
    print("\n[QUEUE STATUS]")
    cmd = f"""psql -U {DB_USER} -d {DB_NAME} -c "SELECT status, COUNT(*) FROM processing_queue GROUP BY status;" """
    print(run(cmd))

def worker():
    print("\n[WORKER STATUS]")
    print(run("ps aux | grep worker | grep -v grep"))

def listener():
    print("\n[LISTENER STATUS]")
    print(run("ps aux | grep telegram_pyro_listener | grep -v grep"))

def system():
    print("\n[SYSTEM MEMORY]")
    print(run("free -h"))

    print("\n[DOCKER]")
    print(run("docker ps"))

def load_hint():
    print("\n[LOAD STATUS]")
    print("Use: python load_engine.py")

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"

    if arg == "queue":
        queue()
    elif arg == "worker":
        worker()
    elif arg == "listener":
        listener()
    elif arg == "system":
        system()
    elif arg == "load":
        load_hint()
    else:
        queue()
        worker()
        listener()
        system()
        load_hint()

if __name__ == "__main__":
    main()
