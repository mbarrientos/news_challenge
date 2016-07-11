FROM python:3.5

RUN apt-get update && apt-get install -y python-psycopg2

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app

CMD run.sh


