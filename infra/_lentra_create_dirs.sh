#!/bin/bash

set -e

echo "[CREATE DIRS] Lentra Agent v1 structure"

mkdir -p /opt/lentra/infra/lentra/telegram/ux/renderers
mkdir -p /opt/lentra/infra/lentra/telegram/ux/router
mkdir -p /opt/lentra/infra/lentra/telegram/session
mkdir -p /opt/lentra/infra/lentra/telegram/delivery
mkdir -p /opt/lentra/infra/lentra/telegram/sql

mkdir -p /opt/lentra/infra/lentra/domain/handlers
mkdir -p /opt/lentra/infra/lentra/domain/agent

echo "[DONE] directories created"

# Git checkpoint (stable snapshot before next stage)
cd /opt/lentra/infra

git add -A

git commit -m "checkpoint: telegram agent v1 step6 structure (ux/session/router)"
git tag stable-step6-ux-v1

echo "[GIT] checkpoint created: stable-step6-ux-v1"
