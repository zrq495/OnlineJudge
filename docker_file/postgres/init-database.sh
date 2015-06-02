gosu postgres postgres --single <<- EOSQL
    CREATE USER oj WITH PASSWORD 'oooo';
    CREATE DATABASE oj;
    GRANT ALL PRIVILEGES ON DATABASE oj TO oj;
    CREATE USER oj_test WITH PASSWORD 'oooo';
    CREATE DATABASE oj_test;
    GRANT ALL PRIVILEGES ON DATABASE oj_test TO oj_test;
EOSQL
