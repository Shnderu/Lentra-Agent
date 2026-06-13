#!/bin/bash

set -e

export PYTHONPATH=/app

exec python -m core.worker.sender_v11
