#!/bin/bash

set -u
ps -ef | grep -Ei 'webserver' | grep -v 'grep' | awk '{print $2}' | xargs -i kill -9 {}
rm -f /opt/airflow/airflow-webserver.pid
