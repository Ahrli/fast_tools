#!/bin/bash

source /usr/local/py37env/bin/activate

set -u
ps -ef | grep -Ei 'webserver' | grep -v 'grep' | awk '{print $2}' | xargs -i kill {}
cd /opt/airflow/
nohup airflow webserver >>/opt/airflow/logs/webserver.log 2>&1 &
#nohup airflow worker >>/opt/airflow/logs/worker.log 2>&1 &
#nohup airflow scheduler >>/opt/airflow/logs/scheduler.log 2>&1 &
