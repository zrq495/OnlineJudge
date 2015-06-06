sudo apt-get install python-pip git python-dev postgresql-9.4 postgresql-server-dev-9.4 redis-server
sudo pip install virtualenv virtualenvwrapper
cat >> ~/.bashrc << EOF
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
  source /usr/local/bin/virtualenvwrapper.sh
fi
EOF
source ~/.bashrc
USER=`whoami`
sudo -u postgres createuser --superuser $USER
sudo -u postgres psql << EOF
alter user $USER with password '$USER';
\q
EOF
sudo -u postgres createdb -O $USER $USER
psql << EOF
CREATE USER oj WITH PASSWORD 'oooo';
CREATE DATABASE oj OWNER oj;
GRANT ALL PRIVILEGES ON DATABASE oj to oj;
CREATE USER oj_test WITH PASSWORD 'oooo';
CREATE DATABASE oj_test OWNER oj_test;
GRANT ALL PRIVILEGES ON DATABASE oj_test to oj_test;
\q
EOF
DATA="/data/"
if [ ! -d "$DATA" ]; then
  sudo mkdir $DATA
  sudo chown $USER:$USER $DATA -R
fi
service redis-server start
source `which virtualenvwrapper.sh`
mkvirtualenv oj
git clone git@github.com:zrq495/OnlineJudge.git
cd OnlineJudge
pip install -r requirements/install.txt
