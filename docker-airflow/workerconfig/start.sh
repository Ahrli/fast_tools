#!/bin/bash

#source /usr/local/py37env/bin/activate
# /root/anaconda3/envs/bibi/bin/python3
conda activate bibi
export C_FORCE_ROOT="true"
set -u
ps -ef | grep -Ei 'airflow' | grep -v 'grep' | awk '{print $2}' | xargs -i kill {}
cd /usr/local/airflow/workerconfig
#nohup airflow webserver >>/opt/airflow/logs/webserver.log 2>&1 &
nohup airflow worker >>/usr/local/airflow/logs/worker.log 2>&1 &
#nohup airflow scheduler >>/opt/airflow/logs/scheduler.log 2>&1 &
