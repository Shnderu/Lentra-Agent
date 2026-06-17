#!/bin/bash

set -e

# remove duplicate presentation logic from core flow
rm -f app/core/ux/response_builder.py
rm -f app/core/ux/result_formatter.py

echo "[OK] Removed duplicated presentation layer from core pipeline"
