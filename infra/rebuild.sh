#!/bin/bash

set -e

echo ">>> STOP CONTAINERS"
docker stop lentra-worker || true
docker rm lentra-worker || true

echo ">>> REBUILD IMAGE"
docker build -t infra-lentra-worker /opt/lentra

echo ">>> START WORKER"
docker run -d \
  --name lentra-worker \
  --network infra_default \
  infra-lentra-worker

echo ">>> DONE"
docker logs --tail 50 lentra-worker
