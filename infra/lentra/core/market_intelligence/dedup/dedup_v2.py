
import hashlib


def build_global_signature(listing: dict) -> str:
    base = f"{listing.get('city')}::{listing.get('location')}::{listing.get('price')}"
    return hashlib.sha256(base.encode()).hexdigest()


def is_duplicate(existing_signatures: set, listing: dict) -> bool:
    sig = build_global_signature(listing)
    return sig in existing_signatures


def register_signature(existing_signatures: set, listing: dict) -> set:
    sig = build_global_signature(listing)
    existing_signatures.add(sig)
    return existing_signatures
