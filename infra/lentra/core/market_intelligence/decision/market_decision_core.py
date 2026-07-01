"""
DEPRECATED: ALL LOGIC MOVED TO AI OS

This module is kept only for compatibility.
"""

from lentra.runtime.intelligence_gateway import interpret


def analyze(payload: dict):
    return interpret(payload)
