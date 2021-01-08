# VERSION 1.10.9
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow

FROM python:3.7-slim-buster
LABEL maintainer="Puckel_"
RUN apt-get install  tzdata
RUN cp -f /usr/share/zoneinfo/Asia/Shanghai     /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone
ENV TZ=Asia/Shanghai


USER airflow

