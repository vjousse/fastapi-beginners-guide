FROM python:3.8-slim
#FROM python:3.6
#ENV PYTHONUNBUFFERED 1
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

MAINTAINER Vincent Porte "vincent@neuralia.co"
ENV REFRESHED_AT 2021-06-15

RUN mkdir -p /config
ADD /config/requirements.pip /config/
RUN pip install --upgrade pip
RUN pip install -r /config/requirements.pip
RUN apt -y update
RUN apt list --upgradable
#RUN apt upgrade
RUN mkdir -p /app
WORKDIR /app