FROM python:2.7
ADD . /OnlineJudge
WORKDIR /OnlineJudge
RUN pip install -r requirements/install.txt
