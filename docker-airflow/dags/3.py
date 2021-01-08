import airflow
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import ExternalTaskSensor
from airflow.models import DAG
from datetime import datetime, timedelta

args = {
    'owner': 'airflow',
    "depends_on_past": False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email': ['657983974@qq.com'],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(seconds=3)
}

dag = DAG(
    dag_id='ll_test_2',
    default_args=args,
    schedule_interval='28 8 * * *'
    )


########################################################## ODS ##########################################################
# 云仓订单
zqp              = BashOperator(
                      task_id = 'adc',
                      bash_command = 'ls',
                      retries=2,
                      dag = dag)