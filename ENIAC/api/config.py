import configparser
import functools
import arrow


cf = configparser.ConfigParser()
configFile = "config/config.ini"
# configFile = "F:\\code_space\\eniac\\factor_server_docker\\ENIAC\\config\\config.ini"
cf.read(configFile)

"配置来源的属性"
#es
dbHost = cf.get("service_es", "db_host")
dbPort = cf.getint("service_es", "db_port")
dbUser = cf.get("service_es", "db_user")
dbPass = cf.get("service_es", "db_pass")



#log_conf
log_conf = cf.get("file", "log_conf")

# kafka
kafkaHost1 = cf.get("service_kafka", "db_host_1")
kafkaHost2 = cf.get("service_kafka", "db_host_2")
kafkaHost3 = cf.get("service_kafka", "db_host_3")
kafkaPort = cf.get("service_kafka", "db_port")
kafkaTopic = cf.get("service_kafka", "db_topic")

kafkaList = [f'{kafkaHost1}:{kafkaPort}',
             f'{kafkaHost2}:{kafkaPort}',
             f'{kafkaHost3}:{kafkaPort}']

# import logging
# import logging.config
#
# logging.config.fileConfig(log_conf)
# logger = logging.getLogger("neo")
#
# import warnings
# warnings.filterwarnings("ignore") # 防止警告输出



