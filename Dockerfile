FROM python:2.7
ENV C_FORCE_ROOT 1
ADD . /OnlineJudge
WORKDIR /OnlineJudge
RUN pip install -r requirements/install.txt
