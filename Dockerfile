FROM python:3.8.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN apt-get update
RUN apt install -y software-properties-common
RUN pip install -r requirements.txt
WORKDIR /usr/src/app
