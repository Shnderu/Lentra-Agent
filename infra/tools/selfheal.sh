#!/bin/bash

ACTION=$1

echo "[SELFHEAL] action received: $ACTION"

case "$ACTION" in

  rebuild_worker)
    echo "[SELFHEAL] rebuilding worker..."
    docker restart lentra-worker-stream
    ;;

  fix_serializer)
    echo "[SELFHEAL] fixing serialization layer..."
    # placeholder for future patch hook
    docker restart lentra-worker-stream
    ;;

  restart_worker)
    echo "[SELFHEAL] restarting worker..."
    docker restart lentra-worker-stream
    ;;

  manual)
    echo "[SELFHEAL] manual intervention required"
    ;;

  *)
    echo "[SELFHEAL] unknown action"
    ;;

esac
