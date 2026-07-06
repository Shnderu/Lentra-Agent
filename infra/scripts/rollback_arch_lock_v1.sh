#!/usr/bin/env bash

set -e

cd /opt/lentra/infra

git reset --hard arch-lock-v1-stable

systemctl daemon-reload
systemctl restart lentra-api
systemctl restart lentra-worker
systemctl restart lentra-bot

echo "[ROLLBACK] restored to arch-lock-v1-stable"
