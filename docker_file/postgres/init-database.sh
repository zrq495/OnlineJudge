gosu postgres postgres --single <<- EOSQL
    CREATE USER oj WITH PASSWORD 'oooo';
    CREATE DATABASE oj;
    GRANT ALL PRIVILEGES ON DATABASE oj TO oj;
EOSQL
