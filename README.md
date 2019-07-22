# FireSQL ![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/nyanpass/firesql.svg) ![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/nyanpass/firesql.svg)
FireSQL is realtime MySQL like Firebase.

# Install
```bash
docker run --name firesql -p 8080:8080 -d nyanpass/firesql
sleep 20
docker exec -t firesql python3 /root/firesql/examples/sync_server.py
```
