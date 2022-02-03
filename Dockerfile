FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD=password\
    MYSQL_DATABASE=test

RUN apt update && apt upgrade -y
RUN apt install -y build-essential wget libmysqlclient-dev libgmp3-dev python3-pip libssl-dev libffi-dev python3-dev

# FROM python:3.9.9
WORKDIR /mysqludf
COPY ./src/ .
COPY ./test/ .
COPY requirements.txt /mysqludf/
RUN pip3 install -r requirements.txt
RUN g++ avg_big_num.cpp -fPIC -lgmp -shared -o /usr/lib/mysql/plugin/big_average.so -I /usr/include/mysql