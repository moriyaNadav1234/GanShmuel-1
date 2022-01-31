## Config GitHub's Webhook
```
# Connect to EC2
ssh -i ~/.ssh/long.vu-github ec2-user@18.185.248.191

# Build docker-image
docker build --no-cache -t webhook .

# Run it
docker stop webhook && docker rm webhook
docker run --rm --name=webhook -w /app -p 8086:8086 -d webhook
docker run -itd --name=webhook -v $pwd:/app/data/ -v /var/run/docker.sock:/var/run/docker.sock -w /app -p 8086:8086 webhook -f /app/data/billing/docker-compose.yaml up -d
docker run -itd -v /var/run/docker.sock:/var/run/docker.sock -v $pwd:/app/data/ docker/compose:1.24.1 -f /app/data/billing/docker-compose.yaml up -d

# Step:
cd root directory
docker-compose -f devOps/docker-compose.yml up -d

# Create webhook service
http://18.185.248.191:8086/webhook
4f122b3a9553837c833cd1b3f763ed2b

# Test webhook:
Push any changed

# Check port open
lsof -i -P -n | grep LISTEN

```

