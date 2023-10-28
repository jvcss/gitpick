docker cp "C:\Users\vitim\Documents\sources\javascript\apps\gitpick\patcher.sql" postgres-container:/tmp/patcher.sql

docker exec -it postgres-container psql -U postgres -d postgres -f /tmp/patcher.sql