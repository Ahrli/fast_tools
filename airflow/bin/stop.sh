#!/bin/bash

set -u
ps -ef | grep -Ei 'airflow' | grep -v 'grep' | awk '{print $2}' | xargs -i kill -9 {}
ps -ef | grep -Ei 'celeryd' | grep -v 'grep' | awk '{print $2}' | xargs -i kill -9 {}
rm -f /opt/airflow/airflow-webserver.pid
