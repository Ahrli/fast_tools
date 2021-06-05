cd /dfs
rm -rf hqp_bigdata
git clone -b test http://gitlab.9tong.com/huxiaoqiang/hqp_bigdata.git

chmod -R 777 ./hqp*
rm -rf /usr/local/airflow/dags/*
cp /dfs/hqp_bigdata/dags/*    /usr/local/airflow/dags/
