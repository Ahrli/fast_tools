import airflow
from airflow import models,settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'admin'
user.email = 'zhangyulei@haoqipei.com'
user.password = 'hqp@123'
#user.superuser = '1'
session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()
