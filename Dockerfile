FROM python:2.7
ENV DEV_DATABASE_URL postgresql+psycopg2://oj:oooo@postgres/oj
ENV DATABASE_URL postgresql+psycopg2://oj:oooo@postgres/oj
ADD . /OnlineJudge
WORKDIR /OnlineJudge
RUN pip install -r requirements/install.txt
WORKDIR src
