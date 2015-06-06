# OnlineJudge

SDUT Online Judge


## develop

OS: Ubuntu 14.04

- bash install.sh
- workon oj
- python manage.py db deploy
- python manage.py runserver
- celery -A oj.core.tasks:celery worker

url: `http://dev.sdutacm.org:5000/`


## docker

- install docker and docker-compose
- docker-compose build
- docker-compose up


## honcho

- bash install.sh
- workon oj
- honcho start


## Note:

- `export OJ_CONFIG="production"`
- `export OJ_SERVER_NAME="oj.sdutacm.org"`, your server name
- `export MAIL_USERNAME="oj@sdutacm.org"`
- `export MAIL_PASSWORD="password"`
- `export OJ_ADMIN="admin@sdutacm.org"`
