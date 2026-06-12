#!/bin/bash

set -e

echo "================ LENTRA AUTO-DIAGNOSTIC ================"
echo ""

echo "[1] WORKER STATUS"
WORKER_STATUS=$(docker ps --format "{{.Names}} {{.Status}}" | grep lentra-worker-stream || true)

if [ -z "$WORKER_STATUS" ]; then
  echo "❌ WORKER NOT RUNNING"
  exit 1
else
  echo "✔ $WORKER_STATUS"
fi

echo ""

echo "[2] TASK STREAM CHECK"
TASKS=$(docker exec lentra-redis redis-cli XLEN stream:rent:tasks)
echo "tasks: $TASKS"

echo ""

echo "[3] RESULTS STREAM CHECK"
RESULTS=$(docker exec lentra-redis redis-cli XLEN stream:rent:results)
echo "results: $RESULTS"

if [ "$RESULTS" -eq 0 ] && [ "$TASKS" -gt 0 ]; then
  echo "❌ PIPELINE BROKEN AFTER WORKER"
  echo "CAUSE: execution failure inside worker process()"
fi

echo ""

echo "[4] TRACE STREAM CHECK"
TRACE=$(docker exec lentra-redis redis-cli XLEN stream:rent:trace)
echo "trace: $TRACE"

echo ""

echo "[5] CONSUMER GROUP STATUS"
PENDING=$(docker exec lentra-redis redis-cli XINFO GROUPS stream:rent:tasks | grep pending | awk '{print $2}' || echo "0")

echo "pending: $PENDING"

if [ "$PENDING" != "0" ] && [ "$PENDING" != "" ]; then
  echo "⚠ PENDING BACKLOG DETECTED"
fi

echo ""

echo "[6] ROOT CAUSE ANALYSIS"

if [ "$TASKS" -gt 0 ] && [ "$RESULTS" -eq 0 ]; then
  echo "🔥 ROOT CAUSE: WORKER EXECUTION FAILURE"
  echo "→ process() is failing before XADD(results)"
  echo "→ likely serialization / TaskContext mismatch / exception in lifecycle"
fi

if [ "$TASKS" -gt 0 ] && [ "$RESULTS" -gt 0 ]; then
  echo "✔ PIPELINE HEALTHY"
fi

if [ "$TASKS" -eq 0 ]; then
  echo "🔥 ROOT CAUSE: INGESTION FAILURE"
fi

echo ""
echo "================ END DIAGNOSTIC ================"
