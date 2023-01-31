FROM amazonlinux:latest

RUN yum install python3 make zip -y
RUN pip3 install virtualenv
COPY . /src
WORKDIR /src
