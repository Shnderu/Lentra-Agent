"""
DEPRECATED ENTRYPOINT
Canonical entrypoint moved to:
lentra.runtime.bootstrap.main
"""

import os
from lentra.runtime.bootstrap.main import main

if __name__ == "__main__":
    os.environ["LENTRA_MODE"] = "ingestion"
    main()
