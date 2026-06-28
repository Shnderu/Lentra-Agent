

import json
import os

STORE_FILE = "/opt/lentra/infra/data/vector_store.json"


def _ensure():
    os.makedirs(os.path.dirname(STORE_FILE), exist_ok=True)


def _load():
    _ensure()
    if not os.path.exists(STORE_FILE):
        return []
    with open(STORE_FILE, "r") as f:
        return json.load(f)


def _save(store):
    _ensure()
    with open(STORE_FILE, "w") as f:
        json.dump(store, f)


def add_listing(listing, embedding):

    store = _load()

    store.append({
        "embedding": embedding,
        "listing": listing
    })

    _save(store)

    print(f"[VECTOR] saved {listing.get('id')}")


def search(query_embedding, top_k=10):

    store = _load()

    print(f"[VECTOR] loaded size={len(store)}")

    if not store:
        return []

    return [item["listing"] for item in store][:top_k]
