#!/bin/bash

set -e

CMD=$1

python -c "
from app.control.orchestrator import Orchestrator

o = Orchestrator()

if '$CMD' == 'start':
    o.start_all()

elif '$CMD' == 'stop':
    o.stop_all()

elif '$CMD' == 'restart':
    o.restart_all()

elif '$CMD' == 'status':
    print(o.status())

else:
    print('Usage: run_system.sh {start|stop|restart|status}')
"
