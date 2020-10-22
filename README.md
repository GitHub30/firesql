# FireSQL ![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/nyanpass/firesql.svg) ![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/nyanpass/firesql.svg)
FireSQL is realtime MySQL like Firebase.



# Docker Compose
https://docs.docker.com/get-docker/
```shell
docker-compose up
```

open browser to query 
http://0.0.0.0:8080/query/SELECT%20*%20FROM%20sakila.actor;






# Install
```bash
# Start MySQL
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=testdb -d mysql --character-set-server=utf8mb4 --collation-server=utf8mb4_bin --server-id=1 --default_authentication_plugin=mysql_native_password

# Start FireSQL
docker run -p 8080:8080 --link mysql -e MYSQL_HOST=mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=testdb -td nyanpass/firesql
```
