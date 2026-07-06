"""
Lentra unified namespace package root.

This module enables deterministic import resolution:
lentra.api
lentra.core
lentra.domain
lentra.infra

DO NOT implement logic here.
"""

import pkgutil

__path__ = pkgutil.extend_path(__path__, __name__)
