import airflow
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import ExternalTaskSensor
from airflow.models import DAG
from datetime import datetime, timedelta

args = {
    'owner': 'airflow',
    "depends_on_past": False,
    'start_date': airflow.utils.dates.days_ago(0),
    #'email': ['biservice@legain.com'],
    #'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=3)
}

dag = DAG(
    dag_id='ll_test',
    default_args=args,
    schedule_interval='10 */1 * * *'
    )


########################################################## ODS ##########################################################
# 云仓订单
zqp              = BashOperator(
                      task_id = 'adc',
                      bash_command = '/root/anaconda3/envs/airflow/bin/python3 /usr/local/airflow/dags/2.py',
                      retries=2,
                      dag = dag)

zqp2              = BashOperator(
                      task_id = 'adc2',
                      bash_command = '/root/anaconda3/envs/airflow/bin/python3 /usr/local/airflow/dags/3.py',
                      retries=2,
                      dag = dag)

zqp3              = BashOperator(
                      task_id = 'adc3',
                      bash_command = '/root/anaconda3/envs/airflow/bin/python3  /usr/local/airflow/dags/2.py',
                      retries=2,
                      dag = dag)

zqp3.set_upstream(zqp)
zqp3.set_upstream(zqp2)



