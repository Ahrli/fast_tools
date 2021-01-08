import airflow
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import ExternalTaskSensor
from airflow.models import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.dingding_operator import DingdingOperator
import pendulum


def failure_callback(context):
    message = 'AIRFLOW TASK FAILURE TIPS:\n' \
              'DAG:    {}\n' \
              'TASKS:  {}\n' \
              'Reason: {}\n' \
        .format(context['task_instance'].dag_id,
                context['task_instance'].task_id,
                context['exception'])
    return DingdingOperator(
        task_id='dingding_success_callback',
        dingding_conn_id='dingding_default',
        message_type='text',
        message=message,
        at_all=True,
    ).execute(context)


local_tz = pendulum.timezone("Asia/Shanghai")  # 设置任务时区
args = {
    'owner': 'airflow',
    "depends_on_past": False,
    'start_date': datetime(2021, 1, 1, tzinfo=local_tz),  # 设置开始时间
    'email': ['657983974@qq.com'],  # 失败发送邮件
    'email_on_failure': False,
    'retries': 1,  # 重试次数 总运行次数=重试次数+1
    'retry_delay': timedelta(seconds=3),  # 重试间隔时间
    'concurrency': 16,  # 调度器允许并发运行的任务实例的数量
    'max_active_runs': 16,  # 每个DAG的最大活动DAG运行次数
    'Catchup': False  # 不回填所有任务

}
# 失败后发送钉钉消息
args['on_failure_callback'] = failure_callback

dag = DAG(
    dag_id='ll_test',
    default_args=args,
    schedule_interval='40 5 * * *' #定义时间 分 时 日 月 周
)

########################################################## ODS ##########################################################
# 测试
zqp = BashOperator(
    task_id='adc',
    bash_command='p',
    retries=2,
    dag=dag)

zqp3 = BashOperator(
    task_id='adc',
    bash_command='p',
    retries=2,
    dag=dag)

# 设置依赖关系
zqp3.set_upstream(zqp)
