#!/bin/bash

set -e

echo "========== WORKER =========="
docker ps --format "table {{.Names}}\t{{.Status}}" | grep lentra || true

echo ""
echo "========== WORKER LOGS =========="
docker logs --tail 50 lentra-worker-stream || true

echo ""
echo "========== STREAM TASKS =========="
docker exec -it lentra-redis redis-cli XRANGE stream:rent:tasks - + || true

echo ""
echo "========== STREAM RESULTS =========="
docker exec -it lentra-redis redis-cli XRANGE stream:rent:results - + || true

echo ""
echo "========== STREAM TRACE =========="
docker exec -it lentra-redis redis-cli XRANGE stream:rent:trace - + || true

echo ""
echo "========== GROUP STATE =========="
docker exec -it lentra-redis redis-cli XINFO GROUPS stream:rent:tasks || true

echo ""
echo "========== CONSUMERS =========="
docker exec -it lentra-redis redis-cli XINFO CONSUMERS stream:rent:tasks workers || true

echo ""
echo "========== PENDING =========="
docker exec -it lentra-redis redis-cli XPENDING stream:rent:tasks workers || true

echo ""
echo "========== STREAM METRICS =========="
docker exec -it lentra-redis redis-cli XINFO STREAM stream:rent:tasks || true
