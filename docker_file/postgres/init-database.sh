psql -h localhost -U postgres -c "CREATE USER oj WITH PASSWORD 'oooo';CREATE DATABASE oj OWNER oj;GRANT ALL PRIVILEGES ON DATABASE oj to oj;"
