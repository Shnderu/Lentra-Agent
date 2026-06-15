#!/bin/bash

set -e

export PYTHONPATH=/opt/lentra/infra

python3 /opt/lentra/infra/lentra/ml/backfill_embeddings.py
