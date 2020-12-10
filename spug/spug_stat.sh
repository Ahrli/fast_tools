#!/bin/bash
docker pull registry.aliyuncs.com/openspug/spug
current_path=$PWD
file_path="/mydata"
path=$current_path$file_path
echo $path
if [ ! -d "$path" ]; then mkdir  $path ; fi
docker run -d --restart=always --name=spug -p 80:80 -v $path:/data registry.aliyuncs.com/openspug/spug
docker exec spug init_spug admin spug.dev
docker restart spug