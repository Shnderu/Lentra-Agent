#!/bin/bash

set -e

CMD=$1

if [ "$CMD" == "start" ]; then
  python -c "from app.control.service_control import ServiceControl; ServiceControl().start_api()"

elif [ "$CMD" == "stop" ]; then
  python -c "from app.control.service_control import ServiceControl; ServiceControl().stop_api()"

elif [ "$CMD" == "restart" ]; then
  python -c "from app.control.service_control import ServiceControl; ServiceControl().restart_api()"

else
  echo "Usage: run.sh {start|stop|restart}"
fi
