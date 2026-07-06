"""
CORE PACKAGE

STRICT RULE:
- no runtime imports
- no guard imports
- no execution layer dependencies
"""

# ONLY domain exports

from .executor import *
from .context import *
