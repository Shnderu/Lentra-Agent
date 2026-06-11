import requests

API_URL = "http://api:8000"


def create_task(payload):
    r = requests.post(f"{API_URL}/task", json=payload)
    return r.json()["task_id"]


def get_task(task_id):
    r = requests.get(f"{API_URL}/task/{task_id}")
    return r.json()
