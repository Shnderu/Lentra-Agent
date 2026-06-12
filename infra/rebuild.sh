#!/bin/bash

set -e

echo ">>> STOP SERVICES"
docker stop lentra-worker 2>/dev/null || true
docker rm lentra-worker 2>/dev/null || true

echo ">>> BUILD IMAGE"
docker build -t infra-lentra-worker /opt/lentra

echo ">>> RUN WORKER (V2 HARDENED)"
docker run -d \
  --name lentra-worker \
  --network infra_default \
  infra-lentra-worker

echo ">>> CHECK LOGS"
sleep 2
docker logs --tail 100 lentra-worker

echo ">>> DONE"
