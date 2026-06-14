#!/bin/bash

echo "[SYSTEM START] LENTRA PIPELINE"

pkill -f dispatcher || true
pkill -f worker || true
pkill -f consumer || true

sleep 1

PYTHONPATH=/opt/lentra/infra python -u /opt/lentra/infra/lentra/telegram/dispatcher.py &
DISPATCHER_PID=$!

PYTHONPATH=/opt/lentra/infra python -u /opt/lentra/infra/lentra/telegram/worker.py &
WORKER_PID=$!

PYTHONPATH=/opt/lentra/infra python -u /opt/lentra/infra/lentra/telegram/delivery/consumer.py &
CONSUMER_PID=$!

echo "[RUNNING]"
echo "dispatcher=$DISPATCHER_PID"
echo "worker=$WORKER_PID"
echo "consumer=$CONSUMER_PID"

wait $DISPATCHER_PID $WORKER_PID $CONSUMER_PID
