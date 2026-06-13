#!/bin/bash

set -e

case "$1" in

  up)
    docker compose up -d --build
    ;;

  down)
    docker compose down
    ;;

  restart-worker)
    docker restart lentra-worker
    ;;

  restart-listener)
    docker restart lentra-listener
    ;;

  logs-worker)
    docker logs -f lentra-worker
    ;;

  logs-listener)
    docker logs -f lentra-listener
    ;;

  rebuild)
    docker compose build
    docker compose up -d
    ;;

  *)
    echo "Usage: dev.sh {up|down|restart-worker|restart-listener|logs-worker|logs-listener|rebuild}"
    ;;
esac
