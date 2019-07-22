# firesql
Cloud Firesql

# Install
```bash
docker run --name firesql -p 8080:8080 -d firesql
sleep 20
docker exec -t firesql python3 /root/firesql/examples/sync_server.py
```
