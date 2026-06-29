#!/bin/bash

set -e

echo "[RESTART] Lentra API service..."

systemctl daemon-reload
systemctl restart lentra-api.service

systemctl status lentra-api.service --no-pager -l
