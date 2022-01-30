## Config GitHub's Webhook
```
# Connect to EC2
ssh -i ~/.ssh/long.vu-github ec2-user@18.185.248.191

# Create webhook service
cd /home/ec2-user/app
python3 -V
python3 -m venv venv
source venv/bin/activate
export FLASK_APP=main.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8086

# Run as service
flask run --host=0.0.0.0 --port=8086 > /dev/null 2>&1

# Check pid and kill
kill -9 <pid>

http://18.185.248.191:8086/webhook
4f122b3a9553837c833cd1b3f763ed2b

# Check port open
lsof -i -P -n | grep LISTEN

```

