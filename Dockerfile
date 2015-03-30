FROM python:2.7
ADD . /OnlineJudge
WORKDIR /OnlineJudge
RUN pip install -r requirements/install.txt
RUN psql -h postgres -U postgres -c "CREATE USER oj WITH PASSWORD 'oooo';CREATE DATABASE oj OWNER oj;GRANT ALL PRIVILEGES ON DATABASE oj to oj;"
