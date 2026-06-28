import hashlib


def build_cluster_signature(features: dict) -> str:
    base = f"{features.get('city')}::{features.get('location')}::{int(features.get('price', 0) // 50)}"
    return hashlib.sha256(base.encode()).hexdigest()


def assign_cluster_local(features: dict) -> str:
    return build_cluster_signature(features)
