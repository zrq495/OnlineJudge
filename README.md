# OnlineJudge
SDUT Online Judge


## How to

- sudo apt-get install pip
- sudo pip install virtualenv virtualenvwrapper
- add follow to ~/.bashrc

	```
	if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
     	source /usr/local/bin/virtualenvwrapper.sh
	fi
	```
- source ~/.bashrc
- sudo apt-get install git
- sudo apt-get install python-dev
- sudo apt-get install postgresql
- sudo -u postgres createuser --superuser zrq495
- sudo -u postgres psql
	- \password zrq495
	- \q
- sudo -u postgres createdb -O zrq495 zrq495
- psql
	- CREATE USER oj WITH PASSWORD 'oooo';
	- CREATE DATABASE oj OWNER oj;
	- GRANT ALL PRIVILEGES ON DATABASE oj to oj;
	- \q
- mkvirtualenv oj
- git clone git@github.com:zrq495/OnlineJudge.git
- cd OnlineJudge
- pip install -r requirements/install.txt
- ./manage.py db deploy
- ./manage.py runserver
- celery -A oj.core.tasks:celery worker


## docker

- mkvirtualenv oj
- pip install -r requirements/install.txt
- docker-compose build
- docker-compose up


## honcho

honcho start
